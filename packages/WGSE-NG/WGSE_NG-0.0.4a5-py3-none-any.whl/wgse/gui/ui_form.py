# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(724, 562)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionLog_viewer = QAction(MainWindow)
        self.actionLog_viewer.setObjectName(u"actionLog_viewer")
        self.actionGenomes = QAction(MainWindow)
        self.actionGenomes.setObjectName(u"actionGenomes")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.informationTab = QWidget()
        self.informationTab.setObjectName(u"informationTab")
        self.gridLayout = QGridLayout(self.informationTab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.progressBar = QProgressBar(self.informationTab)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 1)

        self.fileInformationTable = QTableWidget(self.informationTab)
        self.fileInformationTable.setObjectName(u"fileInformationTable")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileInformationTable.sizePolicy().hasHeightForWidth())
        self.fileInformationTable.setSizePolicy(sizePolicy)
        self.fileInformationTable.setStyleSheet(u"")
        self.fileInformationTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.fileInformationTable.setAlternatingRowColors(True)
        self.fileInformationTable.setShowGrid(True)
        self.fileInformationTable.setGridStyle(Qt.DotLine)
        self.fileInformationTable.setSortingEnabled(False)
        self.fileInformationTable.setColumnCount(0)
        self.fileInformationTable.horizontalHeader().setVisible(False)
        self.fileInformationTable.horizontalHeader().setCascadingSectionResizes(False)
        self.fileInformationTable.horizontalHeader().setStretchLastSection(True)
        self.fileInformationTable.verticalHeader().setVisible(True)
        self.fileInformationTable.verticalHeader().setCascadingSectionResizes(False)
        self.fileInformationTable.verticalHeader().setMinimumSectionSize(30)
        self.fileInformationTable.verticalHeader().setDefaultSectionSize(30)
        self.fileInformationTable.verticalHeader().setHighlightSections(False)
        self.fileInformationTable.verticalHeader().setStretchLastSection(False)

        self.gridLayout.addWidget(self.fileInformationTable, 0, 0, 1, 1)

        self.exportButton = QPushButton(self.informationTab)
        self.exportButton.setObjectName(u"exportButton")

        self.gridLayout.addWidget(self.exportButton, 1, 0, 1, 1)

        self.tabWidget.addTab(self.informationTab, "")
        self.analyzeTab = QWidget()
        self.analyzeTab.setObjectName(u"analyzeTab")
        self.analyzeTab.setEnabled(True)
        self.gridLayout_4 = QGridLayout(self.analyzeTab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.groupBox_5 = QGroupBox(self.analyzeTab)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_3 = QGridLayout(self.groupBox_5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.vcf_annotate = QPushButton(self.groupBox_5)
        self.vcf_annotate.setObjectName(u"vcf_annotate")

        self.gridLayout_3.addWidget(self.vcf_annotate, 1, 3, 1, 1)

        self.label_vcf_modify = QLabel(self.groupBox_5)
        self.label_vcf_modify.setObjectName(u"label_vcf_modify")

        self.gridLayout_3.addWidget(self.label_vcf_modify, 1, 0, 1, 1)

        self.vcf_indel = QPushButton(self.groupBox_5)
        self.vcf_indel.setObjectName(u"vcf_indel")

        self.gridLayout_3.addWidget(self.vcf_indel, 0, 4, 1, 1)

        self.filter_vcf = QPushButton(self.groupBox_5)
        self.filter_vcf.setObjectName(u"filter_vcf")

        self.gridLayout_3.addWidget(self.filter_vcf, 1, 4, 1, 1)

        self.vcf_varqc = QPushButton(self.groupBox_5)
        self.vcf_varqc.setObjectName(u"vcf_varqc")

        self.gridLayout_3.addWidget(self.vcf_varqc, 1, 2, 1, 1)

        self.label_vcf_generate = QLabel(self.groupBox_5)
        self.label_vcf_generate.setObjectName(u"label_vcf_generate")

        self.gridLayout_3.addWidget(self.label_vcf_generate, 0, 0, 1, 1)

        self.vcf_snp = QPushButton(self.groupBox_5)
        self.vcf_snp.setObjectName(u"vcf_snp")

        self.gridLayout_3.addWidget(self.vcf_snp, 0, 3, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_5, 4, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_7, 2, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_8, 2, 2, 1, 1)

        self.groupBox_6 = QGroupBox(self.analyzeTab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.fastp = QPushButton(self.groupBox_6)
        self.fastp.setObjectName(u"fastp")

        self.horizontalLayout_2.addWidget(self.fastp)

        self.fastqc = QPushButton(self.groupBox_6)
        self.fastqc.setObjectName(u"fastqc")

        self.horizontalLayout_2.addWidget(self.fastqc)


        self.gridLayout_4.addWidget(self.groupBox_6, 3, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.analyzeTab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.haplogroup_y = QPushButton(self.groupBox_3)
        self.haplogroup_y.setObjectName(u"haplogroup_y")

        self.horizontalLayout_3.addWidget(self.haplogroup_y)

        self.haplogroup_mito = QPushButton(self.groupBox_3)
        self.haplogroup_mito.setObjectName(u"haplogroup_mito")

        self.horizontalLayout_3.addWidget(self.haplogroup_mito)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)


        self.gridLayout_4.addWidget(self.groupBox_3, 1, 1, 1, 1)

        self.groupBox_4 = QGroupBox(self.analyzeTab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.export_unmapped = QPushButton(self.groupBox_4)
        self.export_unmapped.setObjectName(u"export_unmapped")

        self.horizontalLayout_4.addWidget(self.export_unmapped)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.gridLayout_4.addWidget(self.groupBox_4, 2, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 5, 1, 1, 1)

        self.tabWidget.addTab(self.analyzeTab, "")
        self.extractTab = QWidget()
        self.extractTab.setObjectName(u"extractTab")
        self.gridLayout_2 = QGridLayout(self.extractTab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.y_extract_group = QGroupBox(self.extractTab)
        self.y_extract_group.setObjectName(u"y_extract_group")
        self.y_extract_group.setEnabled(True)
        self.verticalLayout_3 = QVBoxLayout(self.y_extract_group)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.y_bam = QPushButton(self.y_extract_group)
        self.y_bam.setObjectName(u"y_bam")
        self.y_bam.setEnabled(True)

        self.verticalLayout_3.addWidget(self.y_bam)

        self.y_and_mito_bam = QPushButton(self.y_extract_group)
        self.y_and_mito_bam.setObjectName(u"y_and_mito_bam")
        self.y_and_mito_bam.setEnabled(True)

        self.verticalLayout_3.addWidget(self.y_and_mito_bam)

        self.y_vcf = QPushButton(self.y_extract_group)
        self.y_vcf.setObjectName(u"y_vcf")
        self.y_vcf.setEnabled(True)

        self.verticalLayout_3.addWidget(self.y_vcf)


        self.gridLayout_2.addWidget(self.y_extract_group, 6, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 5, 2, 1, 1)

        self.microarray = QPushButton(self.extractTab)
        self.microarray.setObjectName(u"microarray")

        self.gridLayout_2.addWidget(self.microarray, 3, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 7, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 5, 0, 1, 1)

        self.groupBox = QGroupBox(self.extractTab)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.mit_bam = QPushButton(self.groupBox)
        self.mit_bam.setObjectName(u"mit_bam")

        self.verticalLayout_2.addWidget(self.mit_bam)

        self.mito_fasta = QPushButton(self.groupBox)
        self.mito_fasta.setObjectName(u"mito_fasta")

        self.verticalLayout_2.addWidget(self.mito_fasta)

        self.mito_vcf = QPushButton(self.groupBox)
        self.mito_vcf.setObjectName(u"mito_vcf")

        self.verticalLayout_2.addWidget(self.mito_vcf)


        self.gridLayout_2.addWidget(self.groupBox, 5, 1, 1, 1)

        self.pushButton_5 = QPushButton(self.extractTab)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout_2.addWidget(self.pushButton_5, 4, 1, 1, 1)

        self.tabWidget.addTab(self.extractTab, "")
        self.convertTab = QWidget()
        self.convertTab.setObjectName(u"convertTab")
        self.gridLayout_5 = QGridLayout(self.convertTab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_10, 2, 2, 1, 1)

        self.pushButton = QPushButton(self.convertTab)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_5.addWidget(self.pushButton, 1, 1, 1, 1)

        self.pushButton_3 = QPushButton(self.convertTab)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout_5.addWidget(self.pushButton_3, 3, 1, 1, 1)

        self.pushButton_4 = QPushButton(self.convertTab)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout_5.addWidget(self.pushButton_4, 4, 1, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_6, 0, 1, 1, 1)

        self.pushButton_2 = QPushButton(self.convertTab)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout_5.addWidget(self.pushButton_2, 2, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_9, 2, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_5, 5, 1, 1, 1)

        self.tabWidget.addTab(self.convertTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 724, 21))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy1)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionAbout)
        self.menuTools.addAction(self.actionLog_viewer)
        self.menuTools.addAction(self.actionGenomes)

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"WGSE - Genome sequencing data manipulation tool", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionLog_viewer.setText(QCoreApplication.translate("MainWindow", u"Log viewer", None))
        self.actionGenomes.setText(QCoreApplication.translate("MainWindow", u"Reference genomes", None))
        self.exportButton.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.informationTab), QCoreApplication.translate("MainWindow", u"Information", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"VCF File(s)", None))
        self.vcf_annotate.setText(QCoreApplication.translate("MainWindow", u"Annotate", None))
        self.label_vcf_modify.setText(QCoreApplication.translate("MainWindow", u"Modify/Analyze", None))
        self.vcf_indel.setText(QCoreApplication.translate("MainWindow", u"InDel", None))
        self.filter_vcf.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.vcf_varqc.setText(QCoreApplication.translate("MainWindow", u"VarQC", None))
        self.label_vcf_generate.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.vcf_snp.setText(QCoreApplication.translate("MainWindow", u"SNP", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Analyze FASTQ", None))
        self.fastp.setText(QCoreApplication.translate("MainWindow", u"FASTP", None))
        self.fastqc.setText(QCoreApplication.translate("MainWindow", u"FastQC", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Determine Haplogroups", None))
        self.haplogroup_y.setText(QCoreApplication.translate("MainWindow", u"Y Chromosome", None))
        self.haplogroup_mito.setText(QCoreApplication.translate("MainWindow", u"Mitochondrial DNA", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Microbiome (Kaiju/CosmosID)", None))
        self.export_unmapped.setText(QCoreApplication.translate("MainWindow", u"Export unmapped reads", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.analyzeTab), QCoreApplication.translate("MainWindow", u"Analyze", None))
        self.y_extract_group.setTitle(QCoreApplication.translate("MainWindow", u"Y Chromosome", None))
        self.y_bam.setText(QCoreApplication.translate("MainWindow", u"Y only (BAM)", None))
        self.y_and_mito_bam.setText(QCoreApplication.translate("MainWindow", u"Y and Mitochondrial (BAM)", None))
        self.y_vcf.setText(QCoreApplication.translate("MainWindow", u"Y only (VCF)", None))
        self.microarray.setText(QCoreApplication.translate("MainWindow", u"Microarray", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Mitocondrial", None))
        self.mit_bam.setText(QCoreApplication.translate("MainWindow", u"Mitocondrial (BAM)", None))
        self.mito_fasta.setText(QCoreApplication.translate("MainWindow", u"Mitocondrial (FASTA)", None))
        self.mito_vcf.setText(QCoreApplication.translate("MainWindow", u"Mitocondrial (VCF)", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"WES", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.extractTab), QCoreApplication.translate("MainWindow", u"Extract", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"To CRAM", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"To BAM", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"To FASTQ", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"To SAM", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.convertTab), QCoreApplication.translate("MainWindow", u"Convert", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

