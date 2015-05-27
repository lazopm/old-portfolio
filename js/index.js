


function newMessage(){
  $('.group1 p').hide();
  $('.group2').fadeIn();
  $('.invismsg').focus();
  $('.invismsg').bind('input propertychange', function() {
    str=$('.invismsg').val()
    if(str.indexOf('\n')==-1){
      $('.msgarea').text(str);
    }
    else{
      pre=$('.premsg').text()
      text=$('.msgarea').text()
      if(pre=='NAME'){
        $('<span class="donepremsg">'+pre+'</span>'+'<span class="donemsg" id="name">'+text+'</span><br>').insertBefore($('.premsg'))
        $('.invismsg').val('');
        $('.msgarea').text('');
        $('.premsg').hide().text('EMAIL').fadeIn();
      }
      else if(pre=='EMAIL'){
        if (IsEmail(text)==true){
          $('<span class="donepremsg">'+pre+'</span>'+'<span class="donemsg" id="email">'+text+'</span><br>').insertBefore($('.premsg'))
          $('.invismsg').val('');
          $('.msgarea').text('');
          $('.premsg').hide().text('MSG').fadeIn();
        }
        else{
          $('.invismsg').val(text.replace(/(\r\n|\n|\r)/gm,""));
          alert("Please enter a valid email!");
        }
      }
      else{
        $('.invismsg').unbind();

        $.ajax({
          method: "POST",
          url: "message",
          data: { name: $('#name').text(), email: $('#email').text(), msg: $('.msgarea').text() }
        });
        $('.group2').fadeOut(function(){
          $('.group2 br').hide();
          $('.group2 span').hide();
          $('.group2').append('<span>Thank you! I will email you back as soon as possible.</span><br>');
          $('.group2').fadeIn();
        });

      }
    }
  });
  $('.invismsg').focusout(function() {
    $('.invismsg').focus();
  });
}

function IsEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}
