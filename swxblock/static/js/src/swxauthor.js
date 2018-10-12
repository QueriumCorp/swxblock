/* Javascript for SWxAuthor. */
function SWxAuthor(runtime, element, questions) {
    var qu1 = $( "#variant1", element );
    var dm1 = $( ".display_math", qu1 );

    var qu2 = $( "#variant2", element );
    var dm2 = $( ".display_math", qu2 );

    var qu3 = $( "#variant3", element );
    var dm3 = $( ".display_math", qu3 );
  
    switch (questions) {
        case 1:
            qu1.removeClass("problem-empty");
            qu2.addClass("problem-empty");
            qu3.addClass("problem-empty");
            break;
        case 2:
            qu1.removeClass("problem-empty");
            qu2.removeClass("problem-empty");
            qu3.addClass("problem-empty");
            break;
        case 3:
            qu1.removeClass("problem-empty");
            qu2.removeClass("problem-empty");
            qu3.removeClass("problem-empty");
            break;
    }

    if( dm1.html()=="\\(\\)" ){
        dm1.addClass("problem-empty");
    }else{
        dm1.removeClass("problem-empty");
    }

    if( dm2.html()=="\\(\\)" ){
        dm2.addClass("problem-empty");
    }else{
        dm2.removeClass("problem-empty");
    }

    if( dm3.html()=="\\(\\)" ){
        dm3.addClass("problem-empty");
    }else{
        dm3.removeClass("problem-empty");
    }


    /* PAGE LOAD EVENT */
    $(function ($) {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        setTimeout(function () {
            console.info(questions)
        }, 250);
    });
}