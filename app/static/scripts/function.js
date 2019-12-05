function displayloading() {
            document.getElementById("notification_window").innerHTML = "" +
                "<div class=\"joyride-tip-guide\" data-index=\"0\" style=\"visibility: visible; display: block; top: 77.5px; left: 570px;\"><span class=\"joyride-nub\" style=\"display: none;\"></span><div class=\"joyride-content-wrapper\" role=\"dialog\"><ol>\n" +
                "        <h4>\n" +
                "\n" +
                "          Your account is pending creation...\n" +
                "\n" +
                "        </h4>\n" +
                "                <br><p>\n" +
                "                    This can take between 5-10 min.\n" +
                "                </p>\n" +
                "      </ol>\n" +
                "                <img src=\"/static/img/loading.gif\" style=\"width: 35px; height: auto\"> Pending...\n" +
                "            </div></div>\n" +
                "\n" +
                "    <div class=\"joyride-modal-bg\" style=\"display: block;\"></div>"
}

function socketIO() {
      var socket = io.connect('http://' + document.domain + ':' + location.port);

      socket.on( 'connect', function() {
        socket.emit( 'user connect', {
          data: 'User Connected'
        } )

           document.getElementById("testo").innerHTML = "yo"


       var form = $( 'form' ).on( 'submit', function( e ) {
          e.preventDefault()
          let user_name = $( 'input.username' ).val()
          let user_input = $( 'input.message' ).val()
          socket.emit( 'my event', {
            user_name : user_name,
            message : user_input
          } )
          $( 'input.message' ).val( '' ).focus()
        } )
      } )



       socket.on( 'my response', function( msg ) {
        console.log( msg )
        if( typeof msg.user_name !== 'undefined' ) {
          $( 'h3' ).remove()
          $( 'div.message_holder' ).append( '<div><b style="color: #002">'+msg.user_name+'</b> creating</div>' )
        }
      })


 	socket.on( 'create response', function( msg ) {
        console.log( msg )
        if( typeof msg.user_name !== 'undefined' ) {
          $( 'h3' ).remove()
          $( 'div.message_holder' ).append( '<div><b style="color: #002">'+msg.user_name+'</b> created. WELCOME</div>' )
        }
      })


}