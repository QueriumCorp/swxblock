/* Javascript for SWXBlock. */
function SWXStudent(runtime, element, question) {

    console.info( question );

    var handlerUrl = runtime.handlerUrl(element, 'save_grade');

    console.info( handlerUrl );

    var swxblock_block = $('.swxblock_block', element)[0];
    var stepwise_element = $('querium', element)[0];
    var preview_element;
    var preview_element0 = $('.qq_preview0', element)[0];
    var preview_element1 = $('.qq_preview1', element)[0];
    var preview_element2 = $('.qq_preview2', element)[0];
    var star_box = $('.star-box', element)[0];
    var star1 = $('.star1', element)[0];
    var star2 = $('.star2', element)[0];
    var star3 = $('.star3', element)[0];

    var grade=-1;

    switch( question.q_index ){
        case 0:
            preview_element0.classList.remove("preview_hidden");
            preview_element = preview_element0;
            break;
        case 1:
            preview_element1.classList.remove("preview_hidden");
            preview_element = preview_element1;
            break;
        case 2:
            preview_element2.classList.remove("preview_hidden");
            preview_element = preview_element2;
            break;
        default:
            preview_element0.classList.remove("preview_hidden");
            preview_element = preview_element0;
    }

    preview_element0.onclick = previewClicked;
    preview_element1.onclick = previewClicked;
    preview_element2.onclick = previewClicked;
    
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
    
        preview_element0.classList.add("preview_hidden");
        preview_element1.classList.add("preview_hidden");
        preview_element2.classList.add("preview_hidden");

        stepwise_element.style.display = 'block';
        swxblock_block.classList.add("block_working");
        swxblock_block.classList.remove("block_worked");
        setTimeout( function(){
            swxblock_block.scrollIntoView({ behavior:"smooth"});
        }, 250);
        querium.startQuestion( 'OpenStaxHomework', sId, qDef, callbacks, options, stepwise_element );    
    }

    

    // get student id
    var sIdRegEx = /student=(.*?)&/;

    console.info( handlerUrl );

    var tempStudentId = sIdRegEx.exec( handlerUrl );

    console.info( tempStudentId );

    var sId = ( Array.isArray(tempStudentId) && tempStudentId.length>1 ? tempStudentId[1] : "UnknownStudent");

    console.info( sId );

    /* PAGE LOAD EVENT */
    $(function ($) {
        var lastUpdate = localStorage.getItem( 'oscaServerLastSet' );
        if( 
            (!lastUpdate) || // no server assignment update timestamp
            (lastUpdate && ((Date.now() - lastUpdate) > 21600000) ) // if lastUpdate was more than 6 hours ago
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
}

