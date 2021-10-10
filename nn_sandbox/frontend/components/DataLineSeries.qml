import QtQuick.Controls 2.5
import QtCharts 2.3


ChartView {
    title: "Original (Blue) and Estimated (Red) Signals"
    property var eggdata : LineSeries{
        axisX : myAxisx
        axisY : myAxisy
        useOpenGL : true
    }

    property var estimateddata: LineSeries{
        axisX : myAxisx
        axisY :myAxisy
        useOpenGL : true
    }
    // anchors.fill: parent
    antialiasing: true
    legend.visible: true
    ValueAxis{
        id : myAxisx
        min : 0
        max : 0.5
        labelsColor: Qt.rgba(0,0,0,0.9)
    }

    function updateDataset(dataset){
        clear()

    }
    ValueAxis{
        id : myAxisy
        min : -2
        max : 2
        labelsColor: Qt.rgba(0,0,0,0.9)
    }

    function updateDateset(dataset){
        addLineSeries(dataset)
    }

    function updateTrainingDataset(dataset){
        addLineSeries(dataset)
    }

    function addLineSeries(dataset){
        eggdata = createSeries(
        ChartView.SeriesTypeLine,'EEG origin signal',myAxisx,myAxisy
        )
        console.log(EggBridge.dataset_dict['eeg'])
        for (var i = 0 ;i<  EggBridge.dataset_length;i++){ 
            eggdata.append(i*0.5,
            (EggBridge.dataset_dict['eeg'][i])/1000)
        }
    }
    function reset(){
        clear()
        eggdata = createSeries(
        ChartView.SeriesTypeLine,'EEG origin signal',myAxisx,myAxisy
        )
        estimateddata = createSeries(
            ChartView.SeriesTypeLine,'Estimateddata signal',myAxisx,myAxisy
        )
    }
    function clear(){
        removeAllSeries()
    }
}