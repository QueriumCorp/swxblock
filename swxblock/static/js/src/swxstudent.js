/* Javascript for SWXBlock. */
function SWXStudent(runtime, element, question) {

    var handlerUrl = runtime.handlerUrl(element, 'save_grade');
 
    /* PAGE LOAD EVENT */
    $(function ($) {
        localStorage.setItem( "server", "https://stepwiseai04.querium.com/webMathematica/api/")
        var sIdRegEx = /student=(.*?)&/;
        var tempStudentId = sIdRegEx.exec( handlerUrl );
        var sId = ( Array.isArray(tempStudentId) && tempStudentId.length>1 ? tempStudentId[1] : "UnknownStudent");

        var options = {
            hideMenu: true,
            showMe: true,
            assessing: false,
            issueSubmit: false,
            scribbles: false
        };

        function celebrate(stats) {
            console.info("Celebrate", stats);
            $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify(stats),
                success: null
            });
        }
            
        querium.callbacks = {
            success: celebrate
        };

        var qDef = {
            label: ( question.label ? question.label : "" ),
            description: question.description,
            definition: question.definition,
            type: question.qtype,
            mathml: question.mathml,
            hint1: question.hint1,
            hint2: question.hint2,
            hint3: question.hint3
        };

        querium.startQuestion(
            'OpenStaxHomework', 
            sId, 
            qDef, 
            querium.callbacks, 
            options
        );
    });
}

