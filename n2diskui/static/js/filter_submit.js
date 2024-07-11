import { fail } from "assert";
import Swal from "sweetalert2";

export function popUpSuccess(fileDownloadLoc){
    if (fileDownloadLoc && fileDownloadLoc.trim() !== ""){
        Swal.fire({
            icon: 'success',
            title: 'Success',
            text: `File succesfully downloaded to ${fileDownloadLoc}`,
            showConfirmButton: false,
            timer: 1500,
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

function verifyDataBeforeSubmit() {
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
            popUpSuccess(data.fileDownloadLoc);
        } else {
            popUpFailure(data.failureMessage); 
        }
    })
    .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('filter_button').addEventListener('click', verifyDataBeforeSubmit);
});