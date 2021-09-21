#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "functionwidget.h"
#include <QDoubleSpinBox>
#include <QColorDialog>


MainWindow::MainWindow(QWidget *parent) :
	QMainWindow(parent),
	ui(new Ui::MainWindow)
{
	ui->setupUi(this);

	ui->widget->setA(ui->a_doubleSpinBox->value());
	ui->widget->setStep(ui->step_spinBox->value());
	ui->widget->setPenWidth(ui->pen_width_spinBox->value());

	connect(ui->a_doubleSpinBox, SIGNAL(valueChanged(double)), ui->widget, SLOT(valueChanged(double)));
	connect(ui->step_spinBox, SIGNAL(valueChanged(int)), ui->widget, SLOT(stepChanged(int)));
	connect(ui->pen_width_spinBox, SIGNAL(valueChanged(int)), ui->widget, SLOT(penWidthChanged(int)));

}

MainWindow::~MainWindow()
{
	delete ui;
}

void MainWindow::on_build_pushButton_clicked()
{
	ui->widget->setPenColor(QColorDialog::getColor());
}

void MainWindow::on_pushButton_clicked()
{
	ui->widget->setAxesColor(QColorDialog::getColor());
}
