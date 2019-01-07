window.onload = function (e) {
    
    liff.init(function (data) {
        generateChart();
        initializeApp(data);
    });
};

function generateChart(){
    // Preparing data
    var device_dataset = [
        [ "一號溫度機", 5, 1, 2, 4 , 3, 4, 6],
        [ "二號溫度機", 6, 1, 2, 4 , 3, 4, 6],
        [ "三號溫度機", 8, 1, 2, 4 , 3, 4, 6]
    ]
    var device_set = [
        ['一號溫度機', '二號溫度機', '三號溫度機']
    ]

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
        size: {
            height: 2400,
            width: 4800
        },
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
