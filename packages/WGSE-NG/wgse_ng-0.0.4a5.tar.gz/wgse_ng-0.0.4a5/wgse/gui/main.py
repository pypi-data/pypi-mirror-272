import sys
import webbrowser
from pathlib import Path

from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import (QApplication, QFileDialog, QMainWindow,
                               QMessageBox, QTableWidgetItem, QLabel)

from wgse.adapters.alignment_map_file_info_adapter import AlignmentMapFileInfoAdapter
from wgse.adapters.alignment_stats_adapter import AlignmentStatsAdapter
from wgse.adapters.header_adapter import HeaderAdapter
from wgse.adapters.index_stats_adapter import IndexStatsAdapter
from wgse.alignment_map.alignment_map_file import AlignmentMapFile
from wgse.configuration import MANAGER_CFG
from wgse.data.gender import Gender
from wgse.data.sorting import Sorting
from wgse.external import External
from wgse.fasta.reference import Reference
from wgse.gui.alignment_statistics_dialog import AlignmentStatisticsDialog
from wgse.gui.header_dialog import HeaderDialog
from wgse.gui.index_statistics_dialog import IndexStatisticsDialog
from wgse.gui.ui_form import Ui_MainWindow
from wgse.gui.filedrop import Ui_Drop
from wgse.renderers.html_report import HTMLReport

class WGSEWindow(QMainWindow):
    def launch():
        app = QApplication(sys.argv)
        widget = WGSEWindow()
        widget.show()
        sys.exit(app.exec())

    def __init__(
        self,
        parent=None,
        config = MANAGER_CFG.GENERAL,
        external: External = External(),
    ):
        super().__init__(parent)
        self._external = external
        self.config = config
        self.switch_to_main()
        return
        # self.ui = Ui_Drop()
        # self.ui.setupUi(self)
        # self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setCentralWidget(self.ui.groupBox)
        # self.setAcceptDrops(True)

    def switch_to_main(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.fileInformationTable.setAlternatingRowColors(True)

        self.ui.actionDocumentation.triggered.connect(self.on_doc)
        self.ui.actionOpen.triggered.connect(self.on_open)
        self.ui.actionExit.triggered.connect(self.on_close)
        self.ui.actionSettings.triggered.connect(self.on_settings)
        self.ui.fileInformationTable.doubleClicked.connect(self.file_item_clicked)
        self.ui.exportButton.clicked.connect(self.export)
        self.ui.progressBar.hide()

        if self.config.last_path != None:
            self.on_open(self.config.last_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            print("Dropped file:", file_path)
            # Do something with the dropped file


    def export(self):
        if self.current_file is None:
            return
        file_info_adapter = AlignmentMapFileInfoAdapter()
        index_stat_adapter = IndexStatsAdapter()
        alignment_stats_adapter = AlignmentStatsAdapter()
        header_adapter = HeaderAdapter()

        file_info_adapted = file_info_adapter.adapt(self.current_file.file_info)
        index_stat_adapted = index_stat_adapter.adapt(self.current_file.file_info.index_stats)
        alignment_stats_adapted = alignment_stats_adapter.adapt(
            self.current_file.file_info.alignment_stats
        )
        header_adapted = header_adapter.adapt(self.current_file.header)

        html_report = HTMLReport()
        html_page = html_report.make(
            file_info_adapted,
            index_stat_adapted,
            alignment_stats_adapted,
            header_adapted[0],
            header_adapted[1],
            header_adapted[2],
            header_adapted[3],
        )
        current_path = self.current_file.path
        extensions = "".join(current_path.suffixes[:-1])
        name = current_path.stem + extensions + ".html"
        target = current_path.with_name(name)

        with target.open("wt") as f:
            f.write(html_page)
        webbrowser.open(target)
        self.ui.exportButton.setDisabled(True)

    def get_reference_genome_string(self, reference: Reference):
        perfect_match = [x for x in reference.perfect_match.items() if int(x[1]) == 100]
        if len(perfect_match) > 0:
            string = ""
            for genome, percentage_matching in perfect_match:
                string += f"{genome} ({percentage_matching:.1f}%) "
            string = f"{len(perfect_match)} perfect match(es) found."
        else:
            unknown = [x[0] for x in reference.reference_map.items() if len(x[1]) == 0]
            if len(unknown) > 0:
                string = f"Unable to find a match for {len(unknown)} sequence(s)."
            else:
                string = f"Unable to find a perfect match but is possible to build it."
        return string

    def on_close(self):
        MANAGER_CFG.save()
        self.close()

    def closeEvent(self, event=False):
        MANAGER_CFG.save()
        event.accept()

    def on_doc(self):
        webbrowser.open("https://wgse-ng.readthedocs.io", 2)

    def on_open(self, file: Path = False):
        if not file:
            title = "Open file"
            type = "Aligned File (*.bam *.sam *.cram);;"
            type += "Unaligned file (*.fastq);;"
            type += "References (*.fa *.gz *.fna *.fasta)"
            last_path = str(Path.home())
            if self.config.last_path != None:
                if self.config.last_path.is_dir():
                    last_path = str(self.config.last_path)
                else:
                    last_path = str(Path(self.config.last_path).parent)
            file = QFileDialog.getOpenFileName(self, title, last_path, type)
            if file[0] == "":
                return
            file = Path(file[0])

        if not file.exists():
            return
        if not file.is_file():
            return

        self.config.last_path = file
        self.load_aligned(file)

    def on_settings(self):
        pass

    def load_aligned(self, file):
        self.current_file = AlignmentMapFile(Path(file))
        info = self.current_file.file_info

        sorted_string = info.sorted.name
        if info.sorted in [Sorting.Unknown, Sorting.Unsorted]:
            sorted_string += " (Click to sort)"

        indexed_string = str(info.indexed)
        gender_string = info.gender.name
        if not info.indexed:
            indexed_string += " (Click to index)"
            gender_string += " (File is not indexed)"
        else:
            self._gender_determined(info.gender)
        click_to_open = "(Click here to open)"

        size = self.current_file.path.stat().st_size
        size /= 1024**3
        size = f"{size:.1f} GB"

        rows = [
            ("Directory", str(self.current_file.path.parent)),
            ("Filename", str(self.current_file.path.name)),
            ("Size", size),
            ("File Type", info.file_type.name),
            ("Reference", self.get_reference_genome_string(info.reference_genome)),
            ("Gender", gender_string),
            ("Sorted", sorted_string),
            ("Indexed", indexed_string),
            ("Mitochondrial DNA Model", info.mitochondrial_dna_model.name),
            ("Header", click_to_open),
            ("Alignment stats", click_to_open),
            ("Index stats", click_to_open),
            ("Coverage stats", click_to_open),
        ]

        self.ui.fileInformationTable.setRowCount(len(rows))
        self.ui.fileInformationTable.setColumnCount(1)
        for index, row in enumerate(rows):
            header, value = row
            self.ui.fileInformationTable.setVerticalHeaderItem(
                index, QTableWidgetItem(header)
            )
            self.ui.fileInformationTable.setItem(index, 0, QTableWidgetItem(value))

    def file_item_clicked(self, index: QModelIndex):
        if self.current_file is None:
            return
        handlers = {
            "Sorted": self._do_sorting,
            "Indexed": self._do_indexing,
            "Reference": self._show_reference,
            "Header": self._show_header,
            "Alignment stats": self._show_alignment_stats,
            "Index stats": self._show_index_stats,
            "Coverage stats": self._show_coverage_stats,
        }
        item = self.ui.fileInformationTable.verticalHeaderItem(index.row())
        if item.text() not in handlers:
            return
        handlers[item.text()]()

    def _do_sorting(self):
        if self.current_file is None:
            return
        if self.current_file.file_info.sorted not in [
            Sorting.Unknown,
            Sorting.Unsorted,
        ]:
            return

        prompt = QMessageBox()
        prompt.setWindowTitle("File is not sorted")
        prompt.setText("Do you want to sort the file?")
        prompt.setInformativeText("This may take a while.")
        prompt.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        prompt.setDefaultButton(QMessageBox.StandardButton.No)
        choice = QMessageBox.StandardButton(prompt.exec())
        if choice == QMessageBox.StandardButton.No:
            return

    def _do_indexing(self, user_informed=False):
        if self.current_file is None:
            return
        if self.current_file.file_info.indexed:
            return
        if not user_informed:
            prompt = QMessageBox()
            prompt.setWindowTitle("File is not indexed")
            prompt.setText("Do you want to index the file?")
            prompt.setInformativeText("This may take a while.")
            prompt.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            prompt.setDefaultButton(QMessageBox.StandardButton.No)
            choice = QMessageBox.StandardButton(prompt.exec())
            if choice == QMessageBox.StandardButton.No:
                return

        # TODO: move this in another thread
        self.ui.progressBar.setMaximum(0)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        self._external.index(self.current_file.path)
        self.on_open(self.current_file.path)
        self.ui.progressBar.hide()

    def _show_index_stats(self):
        if self.current_file is None:
            return
        if not self.current_file.file_info.indexed:
            prompt = QMessageBox()
            prompt.setWindowTitle("File is not indexed")
            prompt.setText("Index stats are not available if the file is not indexed.")
            prompt.setInformativeText(
                "Do you want to index the file? This may take a while."
            )
            prompt.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            prompt.setDefaultButton(QMessageBox.StandardButton.No)
            choice = QMessageBox.StandardButton(prompt.exec())
            if choice == QMessageBox.StandardButton.No:
                return
            self._do_indexing(user_informed=True)
            self.on_open(self.current_file.path)
        dialog = IndexStatisticsDialog(self)
        dialog.exec(self.current_file.file_info.index_stats)

    def _show_coverage_stats(self):
        return

    def _show_reference(self):
        pass

    def _show_alignment_stats(self):
        if self.current_file is None:
            return
        dialog = AlignmentStatisticsDialog(self)
        dialog.exec(self.current_file.file_info.alignment_stats)

    def _show_header(self):
        if self.current_file is None:
            return
        dialog = HeaderDialog(self)
        dialog.exec(self.current_file.header)

    def _gender_determined(self, gender: Gender):
        male_only = [
            self.ui.y_extract_group,
            self.ui.haplogroup_y,
        ]
        for element in male_only:
            if gender ==Gender.Female:
                element.hide()
            else:
                element.show()