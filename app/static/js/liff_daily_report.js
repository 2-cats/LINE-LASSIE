window.onload = function (e) {
    data = prepareData()
    generateChart(data[0], data[1], data[2]);
    liff.init(function (data) {
        initializeApp(data);
    });
};
function prepareData(){
    // Disassemble the original query
    davice_data_list = davice_data_str.split(',');

    device_count = 0;
    device_name = [];
    device_name_ane_value = [];
    tmp_list = [];

    // Scan array for each item
    for (cnt = 0; cnt < davice_data_list.length; cnt++) { 
        // If item is title
        if (device_count == 0){
            //Push device_name to device name list
            device_name.push(davice_data_list[cnt]);
            tmp_list.push(davice_data_list[cnt]);
        // If item is not title
        }else{
            tmp_list.push(parseInt(davice_data_list[cnt]));
        }

        device_count++;

        //Confirm if it is the next machine
        if (device_count == 25){
            // Complete the array and combine it back
            device_name_ane_value.push(tmp_list);
            // initialization
            device_count = 0;
            tmp_list = [];
        }
    }
    
    var device_set = [
        device_name
    ];

    hours_string = []
    for (cnt = 0; cnt < 24; cnt++) {
        if (cnt % 6 == 0){
            hours_string.push(cnt)
        }else{
            hours_string.push("")
        }
        
    }

    return [device_name_ane_value, device_set, hours_string];
}

function generateChart(device_dataset, device_set){
    
    /* Start bar chart */
    // Generate bar chart
    var bar_chart = c3.generate({
        bindto: '#bar_chart',
        padding: {
            bottom: 40
        },
        data: {
            columns: [],
            type: 'bar',
            groups: device_set
        },
        grid: {
            x: {
                lines: [
                    {value: 0.0, text: '上午十二時'},
                    {value: 5.5, text: '上午六時'},
                    {value: 11.5, text: '下午十二時'},
                    {value: 17.5, text: '下午六時'}
                ]
            }
        },
        axis: {
            x: {
                type: 'category',
                categories: hours_string
            },
        },
        transition: {
            duration: 900
        }
    });

    // chart animation
    setTimeout(function () {
        bar_chart.load({
            columns: device_dataset
        });
    }, 0);
    /* End bar chart */

    /* Start pie chart */
    // Generate pie chart
    var pie_chart = c3.generate({
        bindto: '#pie_chart',
        padding: {
            bottom: 40
        },
        data: {
            columns: [],
            type : 'pie'
        },
        transition: {
            duration: 2000
        }
    });

    // chart animation
    setTimeout(function () {
        pie_chart.load({
            columns: device_dataset
        });
    }, 1000);
    /* End bar chart */
}


function initializeApp(data) {
    document.getElementById('closewindowbutton').addEventListener('click', function () {
        liff.closeWindow();
    });
}
