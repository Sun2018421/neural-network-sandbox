import QtQml 2.12
import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.12
import QtCharts 2.3

import '..'

Page {
    name: 'EEG'
    ColumnLayout{
        RowLayout {
            GroupBox {
                title: 'Settings'
                Layout.fillWidth: true
                GridLayout {
                    anchors.fill: parent
                    columns: 2
                    Label {
                        text: 'Learning Rate:'
                        Layout.alignment: Qt.AlignHCenter
                    }
                    DoubleSpinBox {
                        enabled: true
                        editable: true
                        value: 2
                        from : 0 
                        to : 100
                        onValueChanged: EggBridge.initial_learning_rate = value / 100
                        Component.onCompleted: EggBridge.initial_learning_rate = value / 100
                        Layout.fillWidth: true
                    }
                    Label {
                        text: 'Delays:'
                        Layout.alignment: Qt.AlignHCenter
                    }
                    SpinBox {
                        id: learningRate
                        enabled: true
                        editable: true
                        value: 10
                        from : 0
                        to: 1000
                        onValueChanged: EggBridge.initial_delays = value
                        Component.onCompleted:  EggBridge.initial_delays = value
                        Layout.fillWidth: true
                    }      
                                 
                }

            }
        }
        RowLayout{
                RadioButton{
                    id : signalbutton
                    checked : true
                    text: qsTr("Signals")
                    enabled : EggBridge.has_finished
                    onClicked : EggBridge.plot_idx = 0
                }
                RadioButton{
                    id : differnecebuttion
                    text: qsTr("Difference")
                    enabled : EggBridge.has_finished
                    onClicked : EggBridge.plot_idx = 1
                }
                ExecutionControls {
                    startButton.enabled: EggBridge.has_finished
                    startButton.onClicked: () => {
                        if (EggBridge.plot_idx == 0){
                            EggBridge.start_eeg_algorithm()
                            datalineseries.clear()
                            draw()
                        }
                        else {
                            // datalineseries.reset()
                            // EggBridge.start_eeg_algorithm()
                            // datalineseries.clear()
                            EggBridge.start_eeg_algorithm()
                            datalineseries.clear()
                            datalineseries.reset()
                        }
                        // draw()
                      
                    }
                    stopButton.enabled: !EggBridge.has_finished
                    stopButton.onClicked: EggBridge.stop_eeg_algorithm()
                    Layout.columnSpan: 2
                    Layout.fillWidth: true
                }
                 Label {
                    text: 'Current Training Iteration'
                    Layout.alignment: Qt.AlignHCenter
                }
                Label {
                    text: EggBridge.current_iterations + 1
                    horizontalAlignment: Text.AlignHCenter
                    onTextChanged: () => {
                        datalineseries.estimateddata.append(
                           EggBridge.current_time ,
                           EggBridge.red_line
                        )
                    }   
                }                
        }
        DataLineSeries{
            id: datalineseries
            // width: 700
            Layout.fillWidth: true
            Layout.fillHeight: true
            Component.onCompleted: () =>{
                draw()
                // datalineseries.updateDateset(EggBridge.dataset_dict['eeg'])
            }
   
        }
    }
    function draw(){
        datalineseries.reset()
            draweggdata()
    }

    function draweggdata(){
        for (var i = 0 ;i< 101;i++){ 
            datalineseries.eggdata.append(EggBridge.eeg_time[i],
            EggBridge.dataset_dict['eeg'][i]*0.00001)
        }
    }

}