import QtQml 2.12
import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.12
import QtCharts 2.3

import '..'

Page {
    name: 'Adaptive Noise Cancellation'
    ColumnLayout {
 
        GroupBox {
            title: 'Settings'
            Layout.fillWidth: true
            GridLayout {
                anchors.fill: parent
                columns: 2
                Label {
                    text: 'Initial Learning Rate'
                    Layout.alignment: Qt.AlignHCenter
                }
                DoubleSpinBox {
                    enabled: AncBridge.has_finished
                    editable: true
                    value: 0.2 * 100
                    onValueChanged: AncBridge.initial_learning_rate = value / 100
                    Component.onCompleted: AncBridge.initial_learning_rate = value / 100
                    Layout.fillWidth: true
                }
                Label {
                    text: 'Momentum:'
                    Layout.alignment: Qt.AlignHCenter
                }
                DoubleSpinBox {
                    enabled: AncBridge.has_finished
                    editable: true
                    value: 0.0 * 100
                    from: 0
                    to: 100
                    onValueChanged: AncBridge.momentum_weight = value / 100
                    Component.onCompleted: AncBridge.test_ratio = value / 100
                    Layout.fillWidth: true
                }
            }
        }
        GroupBox {
            title: 'Information'
            Layout.fillWidth: true
            Layout.fillHeight: true
            GridLayout {
                anchors.left: parent.left
                anchors.right: parent.right
                columns: 2
                ExecutionControls {
                    startButton.enabled: AncBridge.has_finished
                    startButton.onClicked: () => {
                        AncBridge.start_anc_algorithm()
                        datalineseriesChart.clear()
                        datalineseriesChart.reset()
                        adaptiveweights.clear()
                        adaptiveweights.reset()
                        // adaptiveweights.clear()
                        // adaptiveweights.reset()
                        // dataChart.clear()
                        // dataChart.updateTrainingDataset(perceptronBridge.training_dataset)
                        // dataChart.updateTestingDataset(perceptronBridge.testing_dataset)
                        // rateChart.reset()
                    }
                    stopButton.enabled: !AncBridge.has_finished
                    stopButton.onClicked: AncBridge.stop_anc_algorithm()
                    Layout.columnSpan: 2
                    Layout.fillWidth: true
                }
                Label {
                    text: 'Current Training Epoch'
                    Layout.alignment: Qt.AlignHCenter
                }
                Label {
                    text: AncBridge.current_iterations + 1
                    horizontalAlignment: Text.AlignHCenter
                    onTextChanged: () => {
                        datalineseriesChart.eggdata.append(
                            AncBridge.current_time,
                            AncBridge.blue_line
                        )
                        datalineseriesChart.estimateddata.append(
                            AncBridge.current_time,
                            AncBridge.red_line
                        )
                        adaptiveweights.eggdata.append(
                            AncBridge.w0
                            ,AncBridge.w1
                        )
                    }
                    Layout.fillWidth: true
                }
            }

        }
         RadioButton{
                id : signalbutton
                checked : true
                text: qsTr("Signals")
                enabled : AncBridge.has_finished
                onClicked : AncBridge.plot_idx = 0
            }
            RadioButton{
                id : differnecebuttion
                text: qsTr("Difference")
                enabled : AncBridge.has_finished
                onClicked : AncBridge.plot_idx = 1
            }
    }
    ColumnLayout {
        DataLineSeries {
            id: datalineseriesChart
            width: 600
            Layout.fillWidth: true
            Layout.fillHeight: true
            function clear() {
                removeAllSeries()
            }
            Component.onCompleted: datalineseriesChart.reset()
        }
        DataLineSeries22 {
            id : adaptiveweights
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }
}