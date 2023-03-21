var container = document.getElementById('histogram');
var nb_vrais_billets = container.getAttribute('data-nb-vrais-billets');
var nb_faux_billets = container.getAttribute('data-nb-faux-billets');

var dataset = [
  { label: "Vrai billet", count: parseInt(nb_vrais_billets) },
  { label: "Faux billet", count: parseInt(nb_faux_billets) }
];

// Nouveau code pour l'histogramme avec Highcharts.js
Highcharts.chart('histogram', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Nombre de vrais et de faux billets'
    },
    xAxis: {
        categories: dataset.map(function (d) { return d.label; }),
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Nombre de billets'
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: [{
        name: 'Billets',
        data: dataset.map(function (d) { return d.count; }),
        colorByPoint: true,
        colors: ['green', 'red']
    }]
});
