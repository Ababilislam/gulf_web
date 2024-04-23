/* Imports */
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";

/* Chart code */
// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end



let container = am4core.create("chartdiv3", am4core.Container);
container.width = am4core.percent(100);
container.height = am4core.percent(100);
container.layout = "vertical";

createBulletChart(container, "solid");
createBulletChart(container, "gradient");

/* Create ranges */
function createRange(axis, from, to, color) {
  let range = axis.axisRanges.create();
  range.value = from;
  range.endValue = to;
  range.axisFill.fill = color;
  range.axisFill.fillOpacity = 0.8;
  range.label.disabled = true;
}

/* Create bullet chart with specified color type for background */
function createBulletChart(parent, colorType) {
  let colors = ["#19d228", "#b4dd1e", "#f4fb16", "#f6d32b", "#fb7116"]; 
  
  /* Create chart instance */
  let chart = container.createChild(am4charts.XYChart);
  chart.paddingRight = 25;

  /* Add data */
  chart.data = [{
    "category": "Evaluation",
    "value": 65,
    "target": 78
  }];

  /* Create axes */
  let categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
  categoryAxis.dataFields.category = "category";
  categoryAxis.renderer.minGridDistance = 30;
  categoryAxis.renderer.grid.template.disabled = true;

  let valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
  valueAxis.renderer.minGridDistance = 30;
  valueAxis.renderer.grid.template.disabled = true;
  valueAxis.min = 0;
  valueAxis.max = 100;
  valueAxis.strictMinMax = true;
  valueAxis.renderer.labels.template.adapter.add("text", function(text) {
    return text + "%";
  }); 
  
  /* 
    In order to create separate background colors for each range of values, 
    you have to create multiple axisRange objects each with their own fill color 
  */
  if (colorType === "solid") {
    let start = 0, end = 20;
    for (var i = 0; i < 5; ++i) {
      createRange(valueAxis, start, end, am4core.color(colors[i]));
      start += 20;
      end += 20;
    }
  }
  /*
    In order to create a gradient background, only one axisRange object is needed
    and a gradient object can be assigned to the axisRange's fill property. 
  */ 
  else if (colorType === "gradient") {
    let gradient = new am4core.LinearGradient();
    for (var i = 0; i < 5; ++i) {
      // add each color that makes up the gradient
      gradient.addColor(am4core.color(colors[i]));
    }
    createRange(valueAxis, 0, 100, gradient);
  }

  /* Create series */
  let series = chart.series.push(new am4charts.ColumnSeries());
  series.dataFields.valueX = "value";
  series.dataFields.categoryY = "category";
  series.columns.template.fill = am4core.color("#000");
  series.columns.template.stroke = am4core.color("#fff");
  series.columns.template.strokeWidth = 1;
  series.columns.template.strokeOpacity = 0.5;
  series.columns.template.height = am4core.percent(25);
  series.columns.template.tooltipText = "{value}"

  let series2 = chart.series.push(new am4charts.LineSeries());
  series2.dataFields.valueX = "target";
  series2.dataFields.categoryY = "category";
  series2.strokeWidth = 0;

  let bullet = series2.bullets.push(new am4charts.Bullet());
  let line = bullet.createChild(am4core.Line);
  line.x1 = 0;
  line.y1 = -40;
  line.x2 = 0;
  line.y2 = 40;
  line.stroke = am4core.color("#000");
  line.strokeWidth = 4; 
}