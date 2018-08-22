/* Javascript for SWxStudio. */
function SWxStudio(runtime, element, question) {
 
    var handlerUrl = runtime.handlerUrl(element, 'save_question');

    $('.save-button', element).click(function(eventObject) {
        var data = {
            label : $('#label', element).val(),
            description : $('#description', element).val(),
            definition : $('#definition', element).val(),
            qtype : $('#qtype', element).val(),
            mathml : $('#mathml', element).val(),
            hint1 : $('#hint1', element).val(),
            hint2 : $('#hint2', element).val(),
            hint3 : $('#hint3', element).val(),
        }

        runtime.notify('save', {state:'start'});
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify(data),
            success: null
        }).done( function(response){
            runtime.notify('save', {state:'end'});
        });
    });

    $('.cancel-button', element).click(function(eventObject) {
        runtime.notify('cancel', {});
    });
 
    /* PAGE LOAD EVENT */
    $(function ($) {
    });
}

