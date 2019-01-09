window.onload = function (e) {
    data = prepareData()
    generateChart(data[0], data[1]);
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
        if (device_count == 8){
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
    return [device_name_ane_value, device_set];
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
                    {value: 0.5},
                    {value: 1.5},
                    {value: 2.5},
                    {value: 3.5},
                    {value: 4.5},
                    {value: 5.5},
                    {value: 6.5}
                ]
            }
        },
        axis: {
            x: {
                type: 'category',
                categories: ['日', '一', '二', '三', '四', '五', '六']
            }
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
