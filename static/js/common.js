$(document).ready(function () {
//   function getCookie(name) {
//     var matches = document.cookie.match(new RegExp(
//       "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
//     ));
//     return matches ? decodeURIComponent(matches[1]) : undefined;
//   }

//   function delete_cookie(cookie_name) {
//     var cookie_date = new Date(); // Текущая дата и время
//     cookie_date.setTime(cookie_date.getTime() - 1);
//     document.cookie = cookie_name += "=; expires=" + cookie_date.toGMTString();
//   }
    var date = new Date;
    date.setDate(date.getDate() + 3);
    document.cookie = "client=True; expires=" + date;
  console.log(document.cookie)
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  window.postForm = function postForm(form, results) {
    url = form.attr('action');
    req = $.ajax({
      method: 'POST',
      url: url,
      data: form.serialize(),
      dataType: 'html',
      success: function (result) {
        getList(results);
        $('.modal').removeClass('open-modal');
        $('#resut').remove();
      }
    });
  };
  window.getForm = function getForm(elem) {
    url = elem.attr('href');
    form = '#' + elem.attr('data-formId');
    req = $.ajax({
      method: 'GET',
      url: url,
      dataType: 'html',
      success: function (result) {
        $("#result").html(result);

        function setUrl() {
          $(form).attr('action', url);
        }
        setTimeout(setUrl, 1000);
      }
    });
  };

  updateList = null;

  window.getList = function getList(elem) {
    url = elem.data('url');
    req = $.ajax({
      method: 'GET',
      url: url,
      dataType: 'html',
      success: function (result) {
        elem.html(result);
        clearInterval(updateList);
        updateList = setInterval(getList, 10000, $('#sessions'), status);
      }
    });
  }
  window.getAjax = function getAjax(url, results) {
    req = $.ajax({
      method: 'GET',
      url: url,
      dataType: 'html',
      success: function (result) {
        getList(results);
      }
    });
  }
  window.bindObj = function bindObj() {
    $('.balance-add').click(function () {
      $('.modal-add-balance').addClass('open-modal');
    });
    $('.close-modal').map(function () {
      $(this).click(function () {
        $('.modal').removeClass('open-modal');
        $('.modal-add-balance').removeClass('open-modal');
      });
    });
    $("*[data-get='form']").on('click', function (e) {
      e.preventDefault();
      getForm($(this));
      $('.modal').addClass('open-modal');
    });
    $("*[data-url]").map(function () {
      getList($(this));
    });
    $('.predefault').on('click', function (e) {
      e.preventDefault();
    })
    $('.open_modal-del').map(function () {
      $(this).click(function (e) {
        e.preventDefault();
        pk = $(this).data('item_pk');
        $('#modal-del-' + pk).addClass('open-modal');
        $('.no-del-' + pk).click(function (e) {
          $('#modal-del-' + pk).removeClass('open-modal');
        });
      });
    });
  };
  bindObj();
});
