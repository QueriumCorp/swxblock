/* Javascript for SWxAuthor. */
function SWxAuthor(runtime, element, question) {
 
    /* PAGE LOAD EVENT */
    $(function ($) {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        setTimeout( function(){
            console.info( question )
        }, 250);
    });
}

