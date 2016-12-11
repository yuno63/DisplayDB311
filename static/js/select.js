function setSensors() {
    var category = $('input[name="seg-1"]:checked').val();
    if ($('input[name="pvss"]:checked').val()=="Yes") {
        var sens = sensorsPVSS[category];
    }else{
       var sens = sensorsDB[category];
    }
    $('#sensors').empty();
    $('#label-sens').text("Group: "+category+"("+sens.length+")");
    $('#lb_save_categ').text("Group: "+category+"("+sens.length+")");
    var txtFilter = document.getElementById("txt_filter").value;
    for (var i = 0; i < sens.length; i++){
        if (~sens[i].toLowerCase().indexOf(txtFilter.toLowerCase())) {
            $('#sensors').append("<option value="+sens[i]+">"+sens[i]+"</option>")
        }
    }
}

function changePvssDb() {
    document.getElementById("txt_filter").value = '';
    setSensors();
    clearSelected();
    var lb_pvss = document.getElementById('lb_pvss');
    var lb_db = document.getElementById('lb_db');
    if ($('input[name="pvss"]:checked').val()=="Yes") {
        lb_pvss.style.fontWeight="bold";
        lb_db.style.fontWeight="normal";
    }else{
        lb_pvss.style.fontWeight="normal";
        lb_db.style.fontWeight="bold";
    }
}

function changeSaveGroup() {
    var lb_selected = document.getElementById('lb_save_selected');
    var lb_categ = document.getElementById('lb_save_categ');
    var lb_all = document.getElementById('lb_save_all');
    if ($('input[name="opt-sens-save"]:checked').val()=="selected") {
        lb_selected.style.fontWeight="bold";
        lb_categ.style.fontWeight="normal";
        lb_all.style.fontWeight="normal";
    }
    else if($('input[name="opt-sens-save"]:checked').val()=="categ"){
        lb_selected.style.fontWeight="normal";
        lb_categ.style.fontWeight="bold";
        lb_all.style.fontWeight="normal";
        $('#id_btn_save').prop("disabled", false);
    }
    else if($('input[name="opt-sens-save"]:checked').val()=="all"){
        lb_selected.style.fontWeight="normal";
        lb_categ.style.fontWeight="normal";
        lb_all.style.fontWeight="bold";
        $('#id_btn_save').prop("disabled", false);
    }
    check_btn_save();
}

$(function(){
    $('input[name=seg-1]').change(function(){
        setSensors();
        setTable();
        setFig3D();
        setFileTab();
    });
});

function setLenSaveSelected(){
    selEl = document.getElementById("sensors-selected");
    $('#lb_save_selected').text("Selected ("+selEl.length+")");
}

function appendSelected(){
    // add new element to list
    var sens = $('select#sensors').val();
    var selEl = document.getElementById("sensors-selected");
    for (var isens=0; isens<sens.length; isens++) {
        var id_coinsided = false;
        for(var i=0; i<selEl.length; i++) {
            if (selEl.options[i].value == sens[isens]) 
                {id_coinsided = true};
        }
        if (!id_coinsided) {
            $('#sensors-selected').append("<option value="+sens[isens]+">"+sens[isens]+"</option>");
            $('#id_clear').prop("disabled", false);
            $('#id_btn_draw').prop("disabled", false);
            $('#id_btn_monit').prop("disabled", false);
            $('#id_btn_save').prop("disabled", false);
        }
    }
    setLenSaveSelected();
    check_btn_save();
//     deselect_all();
};

function select_all(){
    var selEl = document.getElementById("sensors-selected");
    for(var i=0; i<selEl.length; i++) {
        selEl.options[i].selected = true;
    }
}

function deselect_all(){
    var selEl = document.getElementById("sensors-selected");
    for(var i=0; i<selEl.length; i++) {
        selEl.options[i].selected = false;
    }
}

function check_btn_save() {
    setLenSaveSelected();
    var selEl = document.getElementById("sensors-selected");
    if ($('input[name="opt-sens-save"]:checked').val()=="selected") {
        if (selEl.length==0) {
            $('#id_btn_save').prop("disabled", true);
        }
    } 
    var txt = $('#txt_file_name').val();
//     window.alert("---- check_btn_save ------- txt:"+txt+"("+txt.length+")");
    if (txt.length==0) {
        $('#id_btn_save').prop("disabled", true);
    }
}

function clearSelected(){
    select_all();
    $('#sensors-selected').empty();
    $('#id_clear').prop("disabled", true);
    $('#id_btn_draw').prop("disabled", true);
    $('#id_btn_monit').prop("disabled", true);
    check_btn_save();
};

function  setFileTab(){
}

$(function() {
    $('#time1').datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss',
        useCurrent: false,
        defaultDate: '2016-10-01 00:00:00',
        minDate: '2016-05-31 18:14:54',
        maxDate: '2016-10-01 19:08:30'
    });
    $('#time2').datetimepicker({
        format: 'YYYY-MM-DD HH:mm:ss',
        useCurrent: false,
        minDate: '2016-05-31 18:14:54',
        maxDate: '2016-10-01 19:08:30',
        defaultDate: '2016-10-01 19:08:30'
    });
});

function SwitchTab(my_tab, my_content) {
    for(var i=0; i<tabNames.length; i++) {
        document.getElementById('content_'+tabNames[i]).style.display = 'none';
        document.getElementById('tb_'+tabNames[i]).style='background-color:white';
        document.getElementById('tb_'+tabNames[i]).className = '';
    }
    document.getElementById(my_content).style.display = 'block';  
    document.getElementById(my_tab).className = 'active';
    document.getElementById(my_tab).style='background-color:yellow';
};

$(function () {
    $("[data-toggle='tooltip']").tooltip();
});

function setTable() {
    var category = $('input[name="seg-1"]:checked').val();
    $('tbody').empty();

    var sensID = sensorsID[category];
    var sensPVSS = sensorsPVSS[category];
    var sensDBraw = sensorsDBraw[category];
    var sensDescript = sensorsDescript[category];
    var sensStatus = sensorsStatus[category];

    for (var i = 0; i < sensPVSS.length; i++){
        var listDB = [sensID[i], sensPVSS[i], sensDBraw[i], sensDescript[i], "N/A", sensStatus[i]];
        var sensVal = "--"
        indSens = nameTables.indexOf(sensPVSS[i])
        if (indSens>-1) {
            sensVal = dbValue[sensPVSS[i]];
        }
        var row = $("<tr>").append($("<td>").html(sensID[i]))
                            .append($("<td>").html(sensPVSS[i]))
                            .append($("<td>").html(sensDBraw[i]))
                            .append($("<td>").html(sensDescript[i]))
                            .append($("<td>").html(sensVal))
                            .append($("<td>").html(sensStatus[i]));
        $("tbody").append(row);
    }
};

function setFig3D() {
    var category = $('input[name="seg-1"]:checked').val();
    $('#id_show_3D').empty();
    var figName = "";
    switch(category) {
        case 'CRP':
            figName = "LAPP.png";
            break;
        case 'Heater':
            figName = "Heater.png";
            break;
        case 'HighVoltage':
            figName = "CAEN_HighVoltage.png";
            break;
        case 'LAPP':
            figName = "LAPP.png";
            break;
        case 'Led':
            break;
        case 'Levelmeter':
            figName = "Levelmeter.png";
            break;
        case 'Pressure':
            figName = "Pressure.png";
            break;
        case 'Temperature':
            figName = "TE_ribbon_chain_1.png";
//             figName = "TE_CRP_ABCD.png";
            break;
        case 'Thermocouple':
            figName = "Thermocouple.png";
            break;
    }
    cmd = '<img src="https://cdn.rawgit.com/yuno63/DBfiles/master/images/' + 
            figName + '" style="height: 420px; width: 700px;">';
//     cmd = '<img src="media/images/' + figName + '" style="height: 420px; width: 700px;">';
    $('#id_show_3D').append(cmd);
};

function draw() {
    select_all();
    $.ajax({
        type: 'POST',
        url: 'draw/',
        data: {
            mode: JSON.stringify( "draw" ),
            names: JSON.stringify( $('#sensors-selected').val() ),
            time1: $('#time1').val(),
            time2: $('#time2').val(),
            pvss_db: JSON.stringify( $('input[name="pvss"]:checked').val()?"pvss":"db" ),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        // if success post request
        success : function(json) {
            $("#object_draw").empty();
            updateGUI( 'object_draw', json['xx'], json['yy'], json['num_gr'], json['maxX'], 
                json['minY'], json['maxY'], json['xlabels'], json['xsForLabels'], json['names'] )
        },
        // if unsuccess post request
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
    deselect_all();
};

function monitor() {
    select_all();
    $.ajax({
        type: 'POST',
        url: 'draw/',
        data: {
            mode: JSON.stringify( "monitor" ),
            names: JSON.stringify( $('#sensors-selected').val() ),
            time_interval: $('#time_interval').val(),
            time_monitor_shift: JSON.stringify( $('#id_time_monitor_shift').val() ),
            pvss_db: JSON.stringify( $('input[name="pvss"]:checked').val()?"pvss":"db" ),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        // if success post request
        success : function(json) {
            $("#object_draw_monit").empty();

            updateGUI( 'object_draw_monit', json['xx'], json['yy'], json['num_gr'], json['maxX'], 
                json['minY'], json['maxY'], json['xlabels'], json['xsForLabels'], json['names'] )

            $('#id_time_monitor').text(json['maxTstr']);
        },
        // if unsucess post request
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
    deselect_all();
};

function save() {
    select_all();
    $.ajax({
        type: 'POST',
        url: 'draw/',
        data: {
            mode: JSON.stringify( "save" ),
            file_name: $('#txt_file_name').val(),
            names: JSON.stringify( $('#sensors-selected').val() ),
            time1: $('#time1-file').val(),
            time2: $('#time2-file').val(),
            pvss_db: JSON.stringify( $('input[name="pvss"]:checked').val()?"pvss":"db" ),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        // if success post request
        success : function(json) {
            window.alert("---- save success ------- json:"+json);
        },
        // if unsuccess post request
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
    deselect_all();
};


function table() {
    $('#id_btn_table_update').prop("disabled", true);
    $.ajax({
        type: 'POST',
        url: 'table/',
        data: {
            time_table_shift: JSON.stringify( $('#id_time_table_shift').val() ),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success : function(json) {
            $("#id_time_table").text("Access time: "+json['time_table_access_str']);  
            dbValue = json['dbValue'];
            setTable();
            $('#id_btn_table_update').prop("disabled", false);
        },
        error : function(xhr,errmsg,err) {
            $('#id_btn_table_update').prop("disabled", false);
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
};

$(document).on('submit', '#draw_form', function(e){
    e.preventDefault();
    draw();
});

$(document).on('submit', '#draw_monit_form', function(e){
    e.preventDefault();
    // change Start-Stop
    var elem = document.getElementById("id_btn_monit");
    if (elem.textContent=="Start") {
        elem.textContent = "Stop???";
        monitor();
        
        var repetition = $('#repetition_db_access').val();  // s
        timerID = setInterval(monitor, 1000*repetition);
    }
    else {
        elem.textContent = "Start";
        clearInterval(window.timerID);
    }
});

$(document).on('submit', '#draw_save_form', function(e){
    e.preventDefault();
    save();
});

$(document).on('submit', '#show_table_form', function(e){
    e.preventDefault();
    table();
});

