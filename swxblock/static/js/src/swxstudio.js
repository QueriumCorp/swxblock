/* Javascript for SWxStudio. */
function SWxStudio(runtime, element, question) {
    // Stub notify so xblock doesnt crash in dev
    if( typeof runtime.notify === "undefined" ){
        runtime.notify = function(){ console.info(arguments); }
    }
 
    var handlerUrl = runtime.handlerUrl(element, 'save_question');

    $('.save-button', element).click(function(eventObject) {
        var data = {
            label : $('#label', element).val(),
            stimulus : $('#stimulus', element).val(),
            definition : $('#definition', element).val(),
            qtype : $('#qtype', element).val(),
            display_math : $('#display_math', element).val(),
            hint1 : $('#hint1', element).val(),
            hint2 : $('#hint2', element).val(),
            hint3 : $('#hint3', element).val(),

            q1_label : $('#q1_label', element).val(),
            q1_stimulus : $('#q1_stimulus', element).val(),
            q1_definition : $('#q1_definition', element).val(),
            q1_qtype : $('#q1_qtype', element).val(),
            q1_display_math : $('#q1_display_math', element).val(),
            q1_hint1 : $('#q1_hint1', element).val(),
            q1_hint2 : $('#q1_hint2', element).val(),
            q1_hint3 : $('#q1_hint3', element).val(),

            q2_label : $('#q2_label', element).val(),
            q2_stimulus : $('#q2_stimulus', element).val(),
            q2_definition : $('#q2_definition', element).val(),
            q2_qtype : $('#q2_qtype', element).val(),
            q2_display_math : $('#q2_display_math', element).val(),
            q2_hint1 : $('#q2_hint1', element).val(),
            q2_hint2 : $('#q2_hint2', element).val(),
            q2_hint3 : $('#q2_hint3', element).val(),
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

