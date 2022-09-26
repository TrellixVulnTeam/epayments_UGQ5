$(document).ready(function () {
    setMoreInfoBtns();
    setHistoryBtns();
    setUpdateBtns();
});

// sets the update button in update status to submit the update
function setUpdateBtns() {
    let updateBtn = document.querySelectorAll("[id^='update_btn_']");
    updateBtn.forEach(function (btn) {
        let row_num = btn.id.split('_')[2];
        let suborder_number = $('#suborder_' + row_num).attr("data-value");
        // set initial update status option
        let curr_status = $('#status_' + row_num).text();
        $('#updated_status_' + row_num).val(curr_status).change();

        $('#' + btn.id).click(function () {
            curr_status = $('#status_' + row_num).text();
            let update_status = $('#updated_status_' + row_num).val();
            if (curr_status === update_status) {
                alert('Status was the same. Could not update')
            } else {
                $.ajax({
                    type: 'PATCH',
                    url: 'api/v1/status/' + suborder_number,
                    data: JSON.stringify({
                        'status': update_status,
                        'comment': $('#update_comment_' + row_num).val()
                    }),
                    datatype: 'json',
                    success: function () {
                        alert("Status Has Been Updated");
                        $('#update_comment_' + row_num).val('');
                        $("#status_" + row_num).text(update_status);
                        $("#update_status_" + row_num).collapse("hide");
                    },
                });
            }
        });
    });
}

// sets the More Info collapse button to display more info
function setMoreInfoBtns() {
    let moreInfoBtn = document.querySelectorAll("[id^='moreinfo_btn']");
    moreInfoBtn.forEach(function (btn) {
        let id_array = btn.id.split('_');
        let row_num = id_array[2];
        let suborder_number = $('#suborder_' + row_num).attr("data-value");
        $('#' + btn.id).click(function () {
            if (!$('#' + id_array[0] + '_' + row_num).is(":visible")) {
                $.ajax({
                    type: 'POST',
                    url: 'api/v1/more_info/' + suborder_number,
                    success: function (result) {
                        $('#info_' + row_num).html(result['info_tab']);
                    }
                });
            }
        });
    });
}

// sets the history collapse button to display history table
function setHistoryBtns() {
    let historyBtn = document.querySelectorAll("[id^='history_btn']");
    historyBtn.forEach(function (btn) {
        let id_array = btn.id.split('_');
        let row_num = id_array[2];
        let suborder_number = $('#suborder_' + row_num).attr("data-value");
        $('#' + btn.id).click(function () {
            if (!$('#' + id_array[0] + '_' + row_num).is(":visible")) {
                $.ajax({
                    type: 'GET',
                    url: 'api/v1/history/' + suborder_number,
                    success: function (result) {
                        $('#history_body_' + row_num).html(result['history_tab']);
                    }
                });
            }
        });
    });
}