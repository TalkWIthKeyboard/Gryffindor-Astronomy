/**
 * Created by CoderSong on 16/8/22.
 */
$(function () {

    //搜索按钮绑定事件
    $("#searchButton").click(function () {

        var searchText = $('#searchJobId').val();
        location.href = '/log/logShow/search?task=' + searchText;
    })

    //删除按钮绑定时间
    $(".delete-bic-button").click(function () {
        var id = $(this).attr('data-id');

        var isConfirmed = confirm("删除后无法恢复该日志,确认删除这项日志吗?");
        var url = '/log/delete/' + id;
        if (isConfirmed)
        {
            $.ajax({
                url:url,
                type:'DELETE',
                success:function () {
                    window.location.reload();
                }
            })
        }
    })

    //修改密码
    $("#sureChangePassword").click(function () {
        if ( $('#userNewPwd').val() !== $('#userNewPwdRepeat').val() ) {
            alert('两次输入的密码不一致!');
            return;
        }

        if ( $('#userNewPwd').val().length < 6 ) {
          alert('新密码的长度不能小于6位!');
          return;
        }

        var url = '/admin/changePassword';

        $.ajax({
          url: url,
          method: 'PUT',
          data: {
            oldPwd: $('#userOldPwd').val(),
            password: $('#userNewPwd').val()
          },
          success: function(data) {
              if (data.message == 0)
              {
                  alert('用户密码修改成功!');
                  window.location.reload();
              }
              else
              {
                  if (data.message == 1)
                  {
                      alert('原密码输入错误!');
                      window.location.reload();
                  }
              }
          }
        });
    })

    $('.look-log-button').click(function () {
        id = $(this).attr('data-id');
        $.ajax({
            url: '/log/getInfo/' + id,
            method: 'GET',
            success: function (data) {
                $('#description').val(data.content)
            }
        })
    })

})