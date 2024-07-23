import Swal from "sweetalert2";
import moment from "moment";
import $ from "jquery";
import 'daterangepicker';

window.Swal = Swal;
window.$ = $;

export function popUpSuccess(fileDownloadLoc){
    if (fileDownloadLoc && fileDownloadLoc.trim() !== ""){
        Swal.fire({
            icon: 'success',
            title: 'Success',
            text: `${fileDownloadLoc}`,
            showConfirmButton: false,
            timer: 5000,
            position: "bottom-right"
        });
    }
}

export function popUpFailure(failureMessage){
    if (failureMessage && failureMessage.trim() !== ""){
        Swal.fire({
            icon: "error",
            title: "Input is invalid.",
            text: `${failureMessage}`,
            
        });
    }
}

function verifyDataBeforeSubmit(event) {
    event.preventDefault();
    const filterFormData = new FormData(document.getElementById('filter_form'));
    const dataObj = Object.fromEntries(filterFormData.entries())

    fetch('/filter_verify_return_pcap', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ dataObj })
    })
    .then(response => response.json())
    .then(data => {
        if (data.isValid) {
            popUpSuccess(data.message);
        } else {
            popUpFailure(data.message); 
        }
    })
    .catch(error => console.error('Error:', error));
}

export function buildDateRangePicker(){
    $(function(){
        $('input[name="datetimerange"]').daterangepicker({
            timePicker: true,
            startDate: moment().startOf('hour'),
            endDate: moment().startOf('hour').add(32, 'hour'),
            locale: {
                format: 'YYYY-MM-DD HH:mm:ss'
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('filter_button').addEventListener('click', verifyDataBeforeSubmit);
    buildDateRangePicker();
});

