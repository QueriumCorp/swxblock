/* Javascript for SWXBlock. */
function SWXStudent(runtime, element, question) {

    var handlerUrl = runtime.handlerUrl(element, 'save_grade');
    var stepwise_element = $('querium', element)[0];
    var preview_element = $('.qq_preview', element)[0];
    var preview_begin = $('.preview-begin', element)[0];
    var star_box = $('.star-box', element)[0];
    var star1 = $('.star1', element)[0];
    var star2 = $('.star2', element)[0];
    var star3 = $('.star3', element)[0];

    var grade=-1;

    preview_begin.onclick = function(){ 
        var options = {
            hideMenu: true,
            showMe: true,
            assessing: false,
            issueSubmit: false,
            scribbles: false
        };
    
        function celebrate(stats) {
            console.info("Celebrate", stats);
            if( stats.usedShowMe ){
                grade=0;
            }else if( stats.errors==0 && stats.hints==0 ){
                grade=3;
            }else if( stats.errors<2 && stats.hints<3 ){
                grade=2;
            }else{
                grade=1;
            }

            switch( grade ){
                case -1:
                    star_box.style.display = 'none';
                    break;
                case 0:
                    star_box.style.display = 'block';
                    star1.classList.remove('full');
                    star1.classList.remove('half');
                    star2.classList.remove('full');
                    star2.classList.remove('half');
                    star3.classList.remove('full');
                    star3.classList.remove('half');
                    break;
                case 1:
                    star_box.style.display = 'block';
                    star1.classList.add('full');
                    star1.classList.remove('half');
                    star2.classList.remove('full');
                    star2.classList.remove('half');
                    star3.classList.remove('full');
                    star3.classList.remove('half');
                    break;
                case 2:
                    star_box.style.display = 'block';
                    star1.classList.add('full');
                    star1.classList.remove('half');
                    star2.classList.add('full');
                    star2.classList.remove('half');
                    star3.classList.remove('full');
                    star3.classList.remove('half');
                    break;
                case 3:
                    star_box.style.display = 'block';
                    star1.classList.add('full');
                    star1.classList.remove('half');
                    star2.classList.add('full');
                    star2.classList.remove('half');
                    star3.classList.add('full');
                    star3.classList.remove('half');
                    break;
                default:
                    console.error('bad grade value:', grade)
            }
            preview_element.style.display = 'initial';
            stepwise_element.style.display = 'none';

            $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify(stats),
                success: null
            });
        }
            
        var callbacks = {
            success: celebrate
        };
    
        var qDef = {
            label: ( question.q_label ? question.q_label : "" ),
            description: question.q_description,
            definition: question.q_definition,
            type: question.q_type,
            display_math: question.q_display_math,
            hint1: question.q_hint1,
            hint2: question.q_hint2,
            hint3: question.q_hint3
        };
    
        preview_element.style.display = 'none';
        stepwise_element.style.display = 'block';
        querium.startQuestion( 'OpenStaxHomework', sId, qDef, callbacks, options, stepwise_element );    
    }

    localStorage.setItem( "server", "https://stepwiseai04.querium.com/webMathematica/api/")

    // get student id
    var sIdRegEx = /student=(.*?)&/;
    var tempStudentId = sIdRegEx.exec( handlerUrl );
    var sId = ( Array.isArray(tempStudentId) && tempStudentId.length>1 ? tempStudentId[1] : "UnknownStudent");


    /* PAGE LOAD EVENT */
    $(function ($) {
    });
}

