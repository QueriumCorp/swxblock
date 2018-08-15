/* Javascript for SWXBlock. */
function SWXBlock(runtime, element, question) {
 
    var handlerUrl = runtime.handlerUrl(element, 'save_question');

    $('#save', element).click(function(eventObject) {
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

        console.info( data );
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify(data),
            success: null
        });
    });

    /* PAGE LOAD EVENT */
    $(function ($) {
        //$('#definition', element).val("Poop");
    });
}

