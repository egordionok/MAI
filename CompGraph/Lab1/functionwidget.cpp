#include "functionwidget.h"
#include <cmath>
#include <QPainter>
#include <QMouseEvent>
#include <QDebug>

#define PI 3.14159265

// public --------------------------------------------------------------------------------
// Конструктор
FunctionWidget::FunctionWidget(QWidget *parent) : QWidget(parent)
{
	pen_color = Qt::blue;
	axes_color = Qt::black;
	first_open = true;
}

// Функция заданная в задании
double FunctionWidget::f(double phi)
{
	return a * cos(3 * phi) * scale;
}

// getter and setter for a
double FunctionWidget::getA()
{
	return a;
}

void FunctionWidget::setA(double a)
{
	this->a = a;
	this->update();
}

// setter'ы для pen_color, step, pen_width, axes_color
void FunctionWidget::setPenColor(QColor color)
{
	this->pen_color = color;
	this->update();
}

void FunctionWidget::setStep(double step)
{
	this->step = step;
}

void FunctionWidget::setPenWidth(int pen_width)
{
	this->pen_width = pen_width;
}

void FunctionWidget::setAxesColor(QColor axes_color)
{
	this->axes_color = axes_color;
}


// protected -------------------------------------------------------------------------------------------

void FunctionWidget::paintEvent(QPaintEvent *)
{
	QPainter qp(this);
	drawAxes(&qp);
	drawFunction(&qp);
}

void FunctionWidget::mousePressEvent(QMouseEvent *event)
{
	mousePressPoint = event->posF();
}

// Реализация перемещения графика с помощью мышки
void FunctionWidget::mouseMoveEvent(QMouseEvent *event)
{
	center.setX(center.x() + (event->posF().x() - mousePressPoint.x()));
	center.setY(center.y() + (event->posF().y() - mousePressPoint.y()));

	mousePressPoint = event->posF();

	this->update();
}

void FunctionWidget::resizeEvent(QResizeEvent *event)
{
	if (first_open)	// при открытии програмы график рисуется по центру
	{
		center = QPoint(event->size().width() / 2.0, event->size().height() / 2.0);
		first_open = false;
		scale = std::min(width(), height()) / 5;
		axes_scale = scale;
	}
	else // при при расшерении или сжатии график перемещается на половину разности в изм. ширены окна
	{
		center.setX(center.x() + (event->size().width() - event->oldSize().width()) / 2.0);
		center.setY(center.y() + (event->size().height() - event->oldSize().height()) / 2.0);
	}

}

void FunctionWidget::wheelEvent(QWheelEvent *event)
{
	if (event->delta() > 0)
	{
		scale *= 1.2;
		axes_scale *= 1.2;
	}
	else
	{
		scale /= 1.2;
		axes_scale /= 1.2;
	}

	if(std::min(width(), height()) / axes_scale > 10)
	{
		axes_scale *= 2;
	}
	if(std::min(width(), height()) / axes_scale < 4)
	{
		axes_scale /= 2;
	}

	qDebug() << axes_scale;
	this->update();
}

// Процедура для отрисовки заданной функции
void FunctionWidget::drawFunction(QPainter *qp)
{
	double phi = 0;
	QPointF p1(f(phi) * cos(phi), f(phi) * sin(phi));

	QPen pen(pen_color, pen_width, Qt::SolidLine, Qt::RoundCap, Qt::RoundJoin);

	// Отрисовка функции
	qp->setPen(pen);

	for (phi = 0; phi <= PI; phi += PI / step)
	{
		QPointF p2(f(phi) * cos(phi), f(phi) * sin(phi));
		qp->drawLine(p1 + center, p2 + center);
		p1 = p2;
	}

	QPointF p2(f(0) * cos(0), f(0) * sin(0));
	qp->drawLine(p1 + center, p2 + center);
}

void FunctionWidget::drawAxes(QPainter *qp)
{
	QPen pen(Qt::black, 2, Qt::SolidLine, Qt::RoundCap, Qt::RoundJoin);
	QPen axes_pen(Qt::gray, 2, Qt::DotLine, Qt::RoundCap, Qt::RoundJoin);
	qp->setPen(pen);

	QPointF center = this->center;

	// Отрисовка осей координат
	qp->drawLine(QPointF(center.x(), 0), QPointF(center.x(), height()));
	qp->drawLine(QPointF(0, center.y()), QPointF(width(), center.y()));

	double arrow_head_long = std::min(width(), height()) / 35.0;
	double arrow_angle = 15 * PI / 180;
	double axies_angle = 30 * PI / 180;

	// Отрисовка стрелки на ОХ
	qp->drawLine(QPointF(width(), center.y()), QPointF(width() - arrow_head_long * cos(arrow_angle),
													   center.y() - arrow_head_long * sin(arrow_angle)));
	qp->drawLine(QPointF(width(), center.y()), QPointF(width() - arrow_head_long * cos(arrow_angle),
													   center.y() + arrow_head_long * sin(arrow_angle)));

	// Отрисовка стрелки на ОУ
	qp->drawLine(QPointF(center.x(), 0), QPointF(center.x() - arrow_head_long * sin(arrow_angle),
													   arrow_head_long * cos(arrow_angle)));
	qp->drawLine(QPointF(center.x(), 0), QPointF(center.x() + arrow_head_long * sin(arrow_angle),
													   arrow_head_long * cos(arrow_angle)));

	// Отрисовка названия осей
	qp->drawText(QPointF(width() - arrow_head_long * cos(axies_angle),
						 center.y() - arrow_head_long * sin(axies_angle)), "x");
	qp->drawText(QPointF(center.x() + arrow_head_long * sin(axies_angle),
						 arrow_head_long * cos(axies_angle)), "y");

	// Отрисовка шкалы на осях

	qp->drawText(QPointF(center.x() + 5, center.y() - 5), QString::number(0));

	for(int x = axes_scale; x < width() - center.x(); x += axes_scale)
	{
		qp->setPen(axes_pen);
		qp->drawLine(QPointF(center.x() + x, 0), QPointF(center.x() + x, height()));
		qp->setPen(pen);
		qp->drawText(QPointF(center.x() + x, center.y() - 5), QString::number(round(x  * 100 / scale) / 100.));
	}
	for(int x = axes_scale; x < width() + center.x(); x += axes_scale)
	{
		qp->setPen(axes_pen);
		qp->drawLine(QPointF(center.x() - x, 0), QPointF(center.x() - x, height()));
		qp->setPen(pen);
		qp->drawText(QPointF(center.x() - x, center.y() - 5), QString::number(round(-x / scale * 100) / 100.));
	}

	for(int y = axes_scale; y < height() - center.y(); y += axes_scale)
	{
		qp->setPen(axes_pen);
		qp->drawLine(QPointF(0, center.y() + y), QPointF(width(), center.y() + y));
		qp->setPen(pen);
		qp->drawText(QPointF(center.x() + 5, center.y() + y), QString::number(round(-y / scale * 100) / 100.));
	}
	for(int y = axes_scale; y < height() + center.y(); y += axes_scale)
	{
		qp->setPen(axes_pen);
		qp->drawLine(QPointF(0, center.y() - y), QPointF(width(), center.y() - y));
		qp->setPen(pen);
		qp->drawText(QPointF(center.x() + 5, center.y() - y), QString::number(round(y / scale * 100) / 100.));
	}

}

// public slots -------------------------------------------------------------------------------------------

// Слоты для получения параметров от ui
void FunctionWidget::valueChanged(double a)
{
	this->a = a;
	this->update();
}

void FunctionWidget::stepChanged(int step)
{
	if (!step) return;
	this->step = step;
	this->update();
}

void FunctionWidget::penWidthChanged(int pen_width)
{
	if (!pen_width) return;
	this->pen_width = pen_width;
	this->update();
}
