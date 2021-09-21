#ifndef FUNCTION_H
#define FUNCTION_H

#include <QWidget>

class FunctionWidget : public QWidget
{
	Q_OBJECT
public:
	explicit FunctionWidget(QWidget *parent = nullptr);
	double f(double phi);
	double getA();
	void setA(double a);
	void setPenColor(QColor color);
	void setStep(double step);
	void setPenWidth(int pen_width);
	void setAxesColor(QColor axes_color);

protected:
	void paintEvent(QPaintEvent *event);
	void mousePressEvent(QMouseEvent *event);
	void mouseMoveEvent(QMouseEvent *event);
	void resizeEvent(QResizeEvent *event);
	void wheelEvent(QWheelEvent *event);
	void drawFunction(QPainter *qp);
	void drawAxes(QPainter *qp);

public slots:
	void valueChanged(double a);
	void stepChanged(int step);
	void penWidthChanged(int step);

private:
	double	a;					// Коэффицент в уравнении
	int		step;				// Кол-во шагов апроксимации
	int		pen_width;			// Толщина графика
	QColor	pen_color;			// Цвет графика
	QColor	axes_color;			// Цвет осей
	QPointF	center;				// Центр графика
	QPointF	mousePressPoint;	// Точка, в которой произошло нажатие мыши
	bool	first_open;			// Флаг первой отрисовки виджета
	double	scale;				// Масштаб графика
	double	axes_scale;
};

#endif // FUNCTION_H
