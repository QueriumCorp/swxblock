/* Javascript for SWXBlock. */
function SWXStudent(runtime, element, data) {
    // Get our context variables
    var question = data.question;
    var grade = data.grade;
    var solution = data.solution;
    var enable_showme = question.q_option_showme;
    var enable_hint = question.q_option_hint;

    console.info("enable_showme",enable_showme);
    console.info("enable_hint",enable_hint);
    console.info("solution",solution);

    var handlerUrl = runtime.handlerUrl(element, 'save_grade');

    // Get Primary Element Handles
    var swxblock_block = $('.swxblock_block', element)[0];
    var stepwise_element = $('querium', element)[0];

    // Get Active Preview Element Handles
    var preview_element;
    switch( question.q_index ){
        case 0:
            preview_element = $('.qq_preview0', element)[0];
            break;
        case 1:
            preview_element = $('.qq_preview1', element)[0];
            break;
        case 2:
            preview_element = $('.qq_preview2', element)[0];
            break;
        case 3:
            preview_element = $('.qq_preview3', element)[0];
            break;
        case 4:
            preview_element = $('.qq_preview4', element)[0];
            break;
        case 5:
            preview_element = $('.qq_preview5', element)[0];
            break;
        case 6:
            preview_element = $('.qq_preview6', element)[0];
            break;
        case 7:
            preview_element = $('.qq_preview7', element)[0];
            break;
        case 8:
            preview_element = $('.qq_preview8', element)[0];
            break;
        case 9:
            preview_element = $('.qq_preview9', element)[0];
            break;
        default:
            preview_element = $('.qq_preview0', element)[0];
    }

    // Hide Display Math if empty
    var display_math = $('.display-math', preview_element)[0];
    if ( display_math.innerText.length>5 ){
        display_math.classList.remove("preview_hidden");
    }else{
        display_math.classList.add("preview_hidden");
    }

    // Show the active question preview
    preview_element.classList.remove("preview_hidden");
    preview_element.onclick = previewClicked;

    // Get Stat ELement Handles
    var question_stats = $('.question-stats', swxblock_block)[0];
    var star_box = $('.star-box', swxblock_block)[0];
    var star1 = $('.star1', swxblock_block)[0];
    var star2 = $('.star2', swxblock_block)[0];
    var star3 = $('.star3', swxblock_block)[0];
    var elapsed_time_count = $('.elapsed-time-count', swxblock_block)[0];
    var error_count = $('.error-count', swxblock_block)[0];
    var hint_count = $('.hint-count', swxblock_block)[0];
    var used_showme = $('.used-showme', swxblock_block)[0];

    // Get Solution Element Handles
    var solution_element = $('.solution', element)[0];

    // Init preview mode
    updateStats();
    updateSolution();
    
    function previewClicked(){ 
        var options = {
            hideMenu: true,
            showMe: true,
            assessing: false,
            scribbles: false
        };
    
        function celebrate(stats) {
            swxblock_block.classList.remove("block_working");
            swxblock_block.classList.add("block_worked");

            console.info("Celebrate", stats);
            solution = stats;

            if( stats.usedShowMe ){
                grade=0;
            }else if( stats.errors==0 && stats.hints==0 ){
                grade=3;
            }else if( stats.errors<2 && stats.hints<3 ){
                grade=2;
            }else{
                grade=1;
            }

            updateStats();
            updateSolution();

            preview_element.classList.remove("preview_hidden");
            stepwise_element.style.display = 'none';

            stats.grade = grade;

            MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
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
            id: ( question.q_id ? question.q_id : false ),
            label: ( question.q_label ? question.q_label : "" ),
            description: question.q_stimulus,
            definition: question.q_definition,
            type: question.q_type,
            mathml: question.q_display_math,
            hint1: question.q_hint1,
            hint2: question.q_hint2,
            hint3: question.q_hint3
        };
    
        preview_element.classList.add("preview_hidden");
        question_stats.classList.add("preview_hidden");
        solution_element.classList.add("preview_hidden");

        stepwise_element.style.display = 'block';
        swxblock_block.classList.add("block_working");
        swxblock_block.classList.remove("block_worked");
        setTimeout( function(){
            swxblock_block.scrollIntoView({ behavior:"smooth"});
        }, 250);
        querium.startQuestion( 'OpenStaxHomework', sId, qDef, callbacks, options, stepwise_element );    
    }   

    function updateStats(){
        switch( grade ){
            case -1:
                star_box.classList.add("preview_hidden");
                break;
            case 0:
                star_box.classList.remove("preview_hidden");
                star1.classList.remove('full');
                star1.classList.remove('half');
                star2.classList.remove('full');
                star2.classList.remove('half');
                star3.classList.remove('full');
                star3.classList.remove('half');
                break;
            case 1:
                star_box.classList.remove("preview_hidden");
                star1.classList.add('full');
                star1.classList.remove('half');
                star2.classList.remove('full');
                star2.classList.remove('half');
                star3.classList.remove('full');
                star3.classList.remove('half');
                break;
            case 2:
                star_box.classList.remove("preview_hidden");
                star1.classList.add('full');
                star1.classList.remove('half');
                star2.classList.add('full');
                star2.classList.remove('half');
                star3.classList.remove('full');
                star3.classList.remove('half');
                break;
            case 3:
                star_box.classList.remove("preview_hidden");
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

        if( grade==-1 ){
            question_stats.classList.add("preview_hidden");
        }else{
            question_stats.classList.remove("preview_hidden");
            elapsed_time_count.innerText = solution.time.toFixed();
            error_count.innerText = solution.errors;
            hint_count.innerText = solution.hints;
    
            if( solution.usedShowMe ){
                used_showme.classList.remove("preview_hidden");
            }else{
                used_showme.classList.add("preview_hidden");
            }    
        }
    }

    function updateSolution(){
        if( grade==-1 ){ return; }

        // kill solution_element's children
        while (solution_element.firstChild) {
            solution_element.removeChild(solution_element.firstChild);
        }

        // build array of steps
        let step_list = [];
        var c, i, et;
        var new_step_el, step_time_el, step_type_el, step_text_el;

        for( c=0; c<solution.stepDetails.length; c++){
            for( i=0; i<solution.stepDetails[c].info.length; i++){
                console.info( solution.stepDetails[c].info[i])
                // step wrapper
                new_step_el = document.createElement("div");
                new_step_el.classList.add("step-container");

                // time of step
                step_time_el = document.createElement("div");
                step_time_el.classList.add("step-time");
                et = solution.stepDetails[c].info[i].time/1000;
                step_time_el.innerText= et.toFixed() + "s";

                // step details
                step_type_el = document.createElement("div");
                step_type_el.classList.add("step-icon");
                step_text_el = document.createElement("div");
                step_text_el.classList.add("step-text");

                switch( solution.stepDetails[c].info[i].status ){
                    case 0: // victory
                        step_type_el.classList.add("question-completed");
                        step_text_el.innerHTML=solution.stepDetails[c].info[i].mathML
                        break;
                    case 1: // valid step
                        step_type_el.classList.add("valid-step");
                        step_text_el.innerHTML=solution.stepDetails[c].info[i].mathML
                        break;
                    case 3: // invalid step
                        step_type_el.classList.add("invalid-step");
                        step_text_el.innerHTML=solution.stepDetails[c].info[i].mathML
                        break;
                    case 4: // hint request
                        step_type_el.classList.add("hint-request");
                        step_text_el.innerHTML=solution.stepDetails[c].info[i].text
                        break;
                    default:
                        console.error(solution.stepDetails[c].info[i]);
                }

                // assemble elements
                new_step_el.appendChild(step_time_el);
                new_step_el.appendChild(step_type_el);
                new_step_el.appendChild(step_text_el);
                solution_element.appendChild(new_step_el);
            }
        }
        
        if( grade==-1){
            solution_element.classList.add("preview_hidden");
        }else{
            console.info('showing solution')
            solution_element.classList.remove("preview_hidden");
            MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        }
    }

    // set student id
    var sId = ( question.q_user.length>1 ? question.q_user : "UnknownStudent");

    console.info( sId );

    /* PAGE LOAD EVENT */
    $(function ($) {
    });

    // wrap element as core.js may pass a raw element or an wrapped one
    angular.bootstrap($(element), ['querium-stepwise']);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
}

