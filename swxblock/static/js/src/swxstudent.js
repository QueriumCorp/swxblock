/* Javascript for SWXBlock. */
function SWXStudent(runtime, element, data) {
    // Get our context variables
    var question = data.question;
    var grade = data.grade;
    var solution = data.solution;

    console.info( solution );

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

    // Get Star ELement Handles
    var star_box = $('.star-box', swxblock_block)[0];
    var star1 = $('.star1', swxblock_block)[0];
    var star2 = $('.star2', swxblock_block)[0];
    var star3 = $('.star3', swxblock_block)[0];

    // Get Solution Element Handles
    var solution_element = $('.solution', element)[0];
    var solution_details = $('pre', solution_element)[0];

    // Init preview mode
    updateStars();
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

            updateStars();
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
        star_box.classList.add("preview_hidden");

        stepwise_element.style.display = 'block';
        swxblock_block.classList.add("block_working");
        swxblock_block.classList.remove("block_worked");
        setTimeout( function(){
            swxblock_block.scrollIntoView({ behavior:"smooth"});
        }, 250);
        querium.startQuestion( 'OpenStaxHomework', sId, qDef, callbacks, options, stepwise_element );    
    }   

    function updateStars(){
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

    }

    function updateSolution(){
        if( grade==-1){
            solution_element.classList.add("preview_hidden");
        }else{
            solution_element.classList.remove("preview_hidden");
            if( Object.keys(solution).length ){
                solution_details.innerText=JSON.stringify(solution, null, 2);
            }else{
                solution_details.innerText="No solution"
            }      
        }
    }

    // set student id
    var sId = ( question.q_user.length>1 ? question.q_user : "UnknownStudent");

    console.info( sId );

    /* PAGE LOAD EVENT */
    $(function ($) {
        var lastUpdate = localStorage.getItem( 'oscaServerLastSet' );
        if( 
            (!lastUpdate) || // no server assignment update timestamp
            (lastUpdate && ((Date.now() - lastUpdate) > 600000) ) // if lastUpdate was more than 10 minutes ago
        ){ 
            fetch( 'https://editorial.querium.com/cgi-bin/getserver.cgi?appId=OSCA' )
            .then( (resp) => resp.json() )
            .then( function( response ){
                var newServer = response.result;
                console.info('New server assigned:', newServer);
                if( newServer && newServer.length ){
                    localStorage.setItem("server", newServer);
                    localStorage.setItem( 'oscaServerLastSet', Date.now() );
                }
            })
            .catch( function (err) {
                    console.info('Dispatcher ERRORED. Current server value is:', localStorage.getItem("server") );
            });
        }

        function timeSince(date) {
            if( typeof date !== 'number' ){
                return "INVALID-DATE"
            }
            var seconds = Math.floor((new Date() - date) / 1000);
            var interval = Math.floor(seconds / 31536000);
            if (interval > 1) {
                return interval + " years";
            }
            interval = Math.floor(seconds / 2592000);
            if (interval > 1) {
                return interval + " months";
            }
            interval = Math.floor(seconds / 86400);
            if (interval > 1) {
                return interval + " days";
            }
            interval = Math.floor(seconds / 3600);
            if (interval > 1) {
                return interval + " hours";
            }
            interval = Math.floor(seconds / 60);
            if (interval > 1) {
                return interval + " minutes";
            }
            return Math.floor(seconds) + " seconds";
        }
    });

    // wrap element as core.js may pass a raw element or an wrapped one
    angular.bootstrap($(element), ['querium-stepwise']);
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
}

