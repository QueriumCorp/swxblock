/* Javascript for SWXBlock. */
function SWXStudent(runtime, element, question) {

    var handlerUrl = runtime.handlerUrl(element, 'save_grade');
    var swxblock_block = $('.swxblock_block', element)[0];
    console.info(swxblock_block);
    var stepwise_element = $('querium', element)[0];
    var preview_element = $('.qq_preview', element)[0];
    var preview_begin = $('.preview-begin', element)[0];
    var star_box = $('.star-box', element)[0];
    var star1 = $('.star1', element)[0];
    var star2 = $('.star2', element)[0];
    var star3 = $('.star3', element)[0];

    var grade=-1;

    preview_element.onclick = function(){ 
        var options = {
            hideMenu: true,
            showMe: true,
            assessing: false,
            issueSubmit: false,
            scribbles: false
        };
    
        function celebrate(stats) {
            swxblock_block.classList.remove("block_working");
            swxblock_block.classList.add("block_worked");

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
            description: question.q_stimulus,
            definition: question.q_definition,
            type: question.q_type,
            mathml: question.q_display_math,
            hint1: question.q_hint1,
            hint2: question.q_hint2,
            hint3: question.q_hint3
        };
    
        preview_element.style.display = 'none';
        stepwise_element.style.display = 'block';
        swxblock_block.classList.add("block_working");
        swxblock_block.classList.remove("block_worked");
        setTimeout( function(){
            console.info("scrolling");
            swxblock_block.scrollIntoView({ behavior:"smooth"});
        }, 250);
        querium.startQuestion( 'OpenStaxHomework', "Test Student", qDef, callbacks, options, stepwise_element );    
    }


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
        }else{
            console.info(
                'Server already assigned. Current server value is:', 
                localStorage.getItem("server"), 
                'and last updated', 
                timeSince(lastUpdate) 
            );
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
}

