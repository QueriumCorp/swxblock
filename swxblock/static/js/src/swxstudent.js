/* Javascript for SWXBlock. */
function SWXStudent(runtime, element, data) {
    console.info("SWXStudent data",data);
    // Get our context variables
    var question = data.question;
    var grade = data.grade;
    var solution = data.solution;
    var count_attempts = data.count_attempts;
    var enable_showme = question.q_option_showme;
    var enable_hint = question.q_option_hint;
    var max_attempts = question.q_max_attempts;
    var weight = question.q_weight;
    var min_steps = question.q_grade_min_steps_count;
    var min_steps_ded = question.q_grade_min_steps_ded;

    console.info("SWXStudent question",question);
    // console.info("SWXStudent enable_showme",enable_showme);
    // console.info("SWXStudent enable_hint",enable_hint);
    console.info("SWXStudent solution",solution);
    // console.info("SWXStudent count_attempts",count_attempts);
    // console.info("SWXStudent max_attempts",max_attempts);
    console.info("SWXStudent weight ",weight);
    console.info("SWXStudent min steps",min_steps);
    console.info("SWXStudent min steps dec",min_steps_ded);
    console.info("SWXStudent grade",grade);

    if (typeof enable_showme === 'undefined') {
        // console.info("enable_showme is undefined");
        enable_showme = true;
    };
    if (typeof enable_hint === 'undefined') {
        // console.info("enable_hint is undefined");
        enable_hint = true;
    };

    var handlerUrl = runtime.handlerUrl(element, 'save_grade');
    console.info("SWXStudent handlerUrl",handlerUrl);
    var handlerUrlStart = runtime.handlerUrl(element, 'start_attempt');
    console.info("SWXStudent handlerUrlStart",handlerUrlStart);

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

    // Get Statistics Element Handles
    var question_stats = $('.question-stats', swxblock_block)[0];
    var star_box = $('.star-box', swxblock_block)[0];
    var star1 = $('.star1', swxblock_block)[0];
    var star2 = $('.star2', swxblock_block)[0];
    var star3 = $('.star3', swxblock_block)[0];
    var elapsed_time_count = $('.elapsed-time-count', swxblock_block)[0];
    var grade_val = $('.grade-val', swxblock_block)[0];
    var error_count = $('.error-count', swxblock_block)[0];
    var hint_count = $('.hint-count', swxblock_block)[0];
    var used_showme = $('.used-showme', swxblock_block)[0];
    var made_attempts = $('.made-attempts', swxblock_block)[0];

    // Get Solution Element Handles
    var solution_element = $('.solution', element)[0];

    // Init preview mode
    updateStats();
    updateSolution();
    
    function previewClicked(){ 
        var options = {
            hideMenu: true,
            showMe: enable_showme,
            assessing: false,
            scribbles: false
        };
    
        // console.info("SWXstudent previewClicked() started");
        // console.info("SWXstudent previewClicked() count_attempts ",count_attempts);
        // console.info("SWXstudent previewClicked() max_attempts ",max_attempts);
        console.info("SWXstudent previewClicked() weight ",weight);
        console.info("SWXstudent previewClicked() min_steps ",min_steps);
        console.info("SWXstudent previewClicked() min_steps_ded ",min_steps_ded);
        // Don't let student launch question if they've exceeded the limit on question attempts
        if (max_attempts != -1 && count_attempts >= max_attempts) {
            // console.info("SWXstudent previewClicked() too many attempts");
            return;
        };
        // console.info("SWXstudent previewClicked() continues");

        function celebrate(stats) {
            swxblock_block.classList.remove("block_working");
            swxblock_block.classList.add("block_worked");

            console.info("Celebrate", stats);
            solution = stats;
            solution.answered_question = question; // remember the question we answered for the stats display
            // console.info("celebrate solution ", solution);

            // NOTE: We compute the grade here for display purposes, but the Python code on the server also calculates the grade itself.
            //       We could pass all of this info over to the server to avoid this duplication of code, provided we trust these browser-based calcs.

            // TODO: replace this simplistic grading with the real server-graded results
            // if( stats.usedShowMe ){
            //     grade=0.0;
            // }else if( stats.errors==0 && stats.hints==0 ){
            //     grade=3.0;
            // }else if( stats.errors<2 && stats.hints<3 ){
            //     grade=2.0;
            // }else{
            //     grade=1.0;
            // }

	    // // partial deduction for not providing min steps with full credit
            // console.info("celebrate tool check min steps ",min_steps," steps ",stats.stepCount);
	    // if (grade == 3.0 && stats.stepCount < min_steps) {
            //     console.info("celebrate tool tool min steps deduction ",min_steps_ded);
            //     grade=grade-min_steps_ded;
	    // }

            console.log('   start calc grade=',grade);
            grade = 3.0;
            console.log('   stats.errors=',stats.errors,' question.q_grade_errors_count=',quest.q_grade_errors_count,' question.q_grade_errors_ded');
            if (stats.errors>question.q_grade_errors_count) {
                grade=grade-question.q_grade_errors_ded;
            }
            console.log('   stats.hints=',stats.hints,' question.q_grade_hints_count=',quest.q_grade_hints_count,' question.q_grade_hints_ded');
            if (stats.hints>question.q_grade_hints_count) {
                grade=grade-question.q_grade_hints_ded;
            console.log('   stats.usedShowMe=',stats.usedShowMe,' question.q_grade_showme_ded=',question.q_grade_showme_ded);
            if (stats.usedShowMe) {
                grade=grade-question.q_grade_showme_ded;
                console.info('    used showme');
            }

            //  Count valid steps

            var c, i;
            var valid_step_count = 0;

            for( c=0; c<solution.stepDetails.length; c++){
                for( i=0; i<solution.stepDetails[c].info.length; i++){
                    console.info('       i=',i,' c=',c,' info=',solution.stepDetails[c].info[i])
                    switch( solution.stepDetails[c].info[i].status ){
                        case 0: // victory
                            valid_step_count++;
                            break;
                        case 1: // valid step
                            valid_step_count++;
                            break;
                        case 3: // invalid step
                            break;
                        case 4: // hint request
                            break;
                        default:
                            break;
                    }
                }
            }
            console.log('   valid_step_count=',valid_step_count);
            console.log('   question.q_definition=',question.q_definition);
            console.log('   question.q_grade_min_steps_count=',question.q_grade_min_steps_count,' question.q_grade_min_steps_ded=',question.q_grade_min_steps_ded);

            if (grade >= 3.0 && count_valid_steps < question.q_grade_min_steps_count && question.q_definition.indexOf('MatchSpec') > -1 ) {
                grade=grade-question.q_grade_min_steps_ded;
                console.log('   took min_steps deduction after grade=',grade);
            } else {
                console.log('   did not take min_steps deduction after grade=',grade);
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
            
        // Callback when the student begins to work on a problem (e.g. enters a step, clicks "Hint", clicks "Show Solution"
        function start_attempt(status) {

            console.info("start_attempt status=",status)
            //console.info("start_attempt sessionId=",status.sessionId," timeMark=",status.timeMark," action=",a=status.action)

            MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
            $.ajax({
                type: "POST",
                url: handlerUrlStart,
                data: JSON.stringify(status),
                success: null
            });
        }

        var callbacks = {
            success: celebrate,
            start: start_attempt
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
        // console.info("SWXblock previewClicked() count_attempts ",count_attempts);
        data.count_attempts += 1;
        count_attempts = data.count_attempts;
        // console.info("SWXStudent incremented count_attempts ",count_attempts);
        // console.info("SWXblock previewClicked() max_attempts ",max_attempts);
        console.info("SWXblock previewClicked() weight ",weight);
        // console.info("SWXblock previewClicked() calling querium.startQuestion with options ",options);
        querium.startQuestion( 'OpenStaxHomework', sId, qDef, callbacks, options, stepwise_element );    
    }   

    function updateStats(){
        console.info('updateStats:', grade)
        // switch( grade ){
        //    case -1:
        if (grade < 0) {    // Including undefined ie. -1
                star_box.classList.add("preview_hidden");
        //      break;
        } else if ( grade > 0.0 && grade < 0.5 ) {
        //    case 0:
                star_box.classList.remove("preview_hidden");
                star1.classList.remove('half');
                star1.classList.remove('full');
                star2.classList.remove('half');
                star2.classList.remove('full');
                star3.classList.remove('half');
                star3.classList.remove('full');
        //      break;
        } else if ( grade >= 0.5 && grade < 1.0 ) {
                star_box.classList.remove("preview_hidden");
                star1.classList.add('half');
                star1.classList.remove('full');
                star2.classList.remove('half');
                star2.classList.remove('full');
                star3.classList.remove('half');
                star3.classList.remove('full');
        } else if ( grade >= 1.0 && grade < 1.5 ) {
        //    case 1:
                star_box.classList.remove("preview_hidden");
                star1.classList.remove('half');
                star1.classList.add('full');
                star2.classList.remove('half');
                star2.classList.remove('full');
                star3.classList.remove('half');
                star3.classList.remove('full');
        //      break;
        } else if ( grade >= 1.5 && grade < 2.0 ) {
                star_box.classList.remove("preview_hidden");
                star1.classList.remove('half');
                star1.classList.add('full');
                star2.classList.add('half');
                star2.classList.remove('full');
                star3.classList.remove('half');
                star3.classList.remove('full');
        } else if ( grade >= 2.0 && grade < 2.5 ) {
        //    case 2:
                star_box.classList.remove("preview_hidden");
                star1.classList.remove('half');
                star1.classList.add('full');
                star2.classList.remove('half');
                star2.classList.add('full');
                star3.classList.remove('half');
                star3.classList.remove('full');
        } else if ( grade >= 2.5 && grade < 3.0 ) {
                star_box.classList.remove("preview_hidden");
                star1.classList.remove('half');
                star1.classList.add('full');
                star2.classList.remove('half');
                star2.classList.add('full');
                star3.classList.add('half');
                star3.classList.remove('full');
        } else if ( grade == 3.0 ) {
        //    case 3:
                star_box.classList.remove("preview_hidden");
                star1.classList.remove('half');
                star1.classList.add('full');
                star2.classList.remove('half');
                star2.classList.add('full');
                star3.classList.remove('half');
                star3.classList.add('full');
        //      break;
        } else if ( grade > 3.0 ) {
        //    default:
                star_box.classList.add("preview_hidden");
                console.error('bad grade value > 3.0:', grade)
        }

        if( grade==-1 ){
            question_stats.classList.add("preview_hidden");
        }else{
            question_stats.classList.remove("preview_hidden");
            elapsed_time_count.innerText = solution.time.toFixed(0);
            // Grade normalized to 1.0 and weighted
            grade_val.innerText = ((grade/3.0)*weight).toFixed(2);
            error_count.innerText = solution.errors;
            hint_count.innerText = solution.hints;
            var attempts_string;
            attempts_string = count_attempts;
            attempts_string += ' of ';
            if( max_attempts == -1) {
               attempts_string += 'unlimited';
            }else{
               attempts_string += max_attempts;
            }
            attempts_string += ' attempts';
            made_attempts.innerText = attempts_string;
    
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

        // Display the stimulus of the problem corresponding to these steps, since the question variant shown may be different
        // than the one used in the attempt associated with these steps/stats.
        var stimulus_el, stimulus_el_text, stimulus_el_problem, stimulus_el_math;
        if (typeof solution.answered_question === 'undefined') {
            // console.info("solution.answered_question is undefined");
        } else {
            stimulus_el = document.createElement("div");
            stimulus_el.classList.add("stimulus");
            stimulus_el_text = document.createElement("div");
            stimulus_el_text.classList.add("stimulus-text");
            stimulus_el_text.innerText= "Last problem attempt was:";
            stimulus_el_problem = document.createElement("div");
            stimulus_el_problem.classList.add("stimulus-problem");
            stimulus_el_problem.innerHTML= solution.answered_question.q_stimulus;
            stimulus_el_math = document.createElement("div");
            stimulus_el_math.classList.add("stimulus-math");
            stimulus_el_math.innerText= solution.answered_question.q_display_math;
            stimulus_el.appendChild(stimulus_el_text);
            stimulus_el.appendChild(stimulus_el_problem);
            stimulus_el.appendChild(stimulus_el_math);
            solution_element.appendChild(stimulus_el);
        };

        // build array of steps
        let step_list = [];
        var c, i, et;
        var new_step_el, step_time_el, step_type_el, step_text_el;

        for( c=0; c<solution.stepDetails.length; c++){
            for( i=0; i<solution.stepDetails[c].info.length; i++){
                // console.info( solution.stepDetails[c].info[i])
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
                        step_text_el.innerHTML=badMathmlFix(solution.stepDetails[c].info[i].text);
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
            // console.info('showing solution')
            solution_element.classList.remove("preview_hidden");
            MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        }
    }

    // StepWise hints can contain bath <mspace> tags and badly escaped > at the end of mathml tags
    function badMathmlFix( s ) {
        // console.debug( 'badmathmlfix in s=',s);
        var goods = s.replace(new RegExp('mspace width=\'\\.\\d+em\'', 'g'), 'MSPACE').replace(new RegExp('MSPACE\\\\', 'g'), 'MSPACE').replace(new RegExp('MSPACE','g'),'mspace width=\'.04em\'').replace(new RegExp('\\\>', 'g'), '>');
        // console.debug( 'badmathmlfix out s=',goods);
        return goods;
    }

    // set student id
    var sId = ( question.q_user.length>1 ? question.q_user : "UnknownStudent");

    // console.info( sId );

    /* PAGE LOAD EVENT */
    $(function ($) {
    });

    // wrap element as core.js may pass a raw element or an wrapped one
    angular.bootstrap($(element), ['querium-stepwise']);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
}
