


function change_progress_to_value(percentage){

    // Get the color value of .element:before
    var progress = window.getComputedStyle(
        document.querySelector('.progress'), '::after'
    ).getPropertyValue('left');

    progress.setValue("${percentage}%"):
}