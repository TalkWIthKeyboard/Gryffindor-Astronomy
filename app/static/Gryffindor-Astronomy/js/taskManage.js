/**
 * Created by CoderSong on 16/8/19.
 */

$(function () {

    $('.form_date').datetimepicker({
        language:  'zh-CN',
        weekStart: 1,
        todayBtn:  1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        minView: 2,
        forceParse: 0
    });

    //时间格式化处理
    Date.prototype.format = function(format){
        var o = {
            "M+" : this.getMonth()+1, //month
            "d+" : this.getDate(), //day
            "h+" : this.getHours(), //hour
            "m+" : this.getMinutes(), //minute
            "s+" : this.getSeconds(), //second
            "q+" : Math.floor((this.getMonth()+3)/3), //quarter
            "S" : this.getMilliseconds() //millisecond
        }

        if(/(y+)/.test(format)) {
            format = format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
        }

        for(var k in o) {
            if(new RegExp("("+ k +")").test(format)) {
                format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
            }
        }
        return format;
    };

    var date = new Date().format("yyyy-MM-dd");
    var start_btn = -1;
    start_btn = $('#start-system-Bt').attr('data-id');
    //页面初始化
    $('.start-button').each(function () {

        var endDate = $(this).attr('data-date');
        if (endDate < date || start_btn == 0)
        {
            $(this).attr('disabled',true)
        }
    });

    //启动系统开关
    $("#start-system-Bt").click(function () {
        $.ajax({
            url: '/taskManage/startSystem',
            type: 'GET',
            success:function () {
                window.location.reload()
            }
        })
    });

    //暂停系统开关
    $("#stop-system-Bt").click(function () {
        $.ajax({
            url: '/taskManage/stopSystem',
            type: 'GET',
            success:function () {
                window.location.reload()
            }
        })
    })

    //开启任务按钮绑定事件
    $(".start-button").click(function () {

        var id = $(this).attr('data-id');
        $.ajax({
            url : '/taskManage/startTask/' + id,
            type : 'GET',
            success: function () {
                window.location.reload()
            }
        })
    });

    //暂停任务按钮绑定事件
    $(".stop-button").click(function () {

        var id = $(this).attr('data-id');
        $.ajax({
            url : '/taskManage/stopTask/' + id,
            type : 'GET',
            success: function () {
                window.location.reload()
            }
        })
    });

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

    //创建提交
    $("#createBicBt").click(function () {

        if (!$('#jobId').val())
        {
            alert("任务编号没有填写");
            return;
        }

        var beginDate = $('#beginDate').val()
        var endDate = $('#endDate').val()
        if (beginDate > endDate)
        {
            alert('起始日期必须小于等于结束日期');
            return;
        }

        var time = $('#pushTime').val()
        if (!time.match(/^[0-9]{2}:[0-9]{2}:[0-9]{2}$/))
        {
            alert('推送时间的格式有误');
            return;
        }

        var url = '/taskManage/create';
        $.ajax({
            url:url,
            type:'POST',
            data: {
                'jobId':$('#jobId').val(),
                'pushTime':$('#pushTime').val(),
                'beginDate':$('#beginDate').val(),
                'endDate':$('#endDate').val(),
                'command':$('#command').val(),
                'description':$('#description').val()
            },
            success:function (rep) {
                //刷新页面
                window.location.reload()
            }
        })
    });

    //更新提交
    $("#updateBicBt").click(function () {

        if (!$('#jobId').val())
        {
            alert("任务编号没有填写");
            return;
        }

        var beginDate = $('#beginDate').val()
        var endDate = $('#endDate').val()
        if (beginDate > endDate)
        {
            alert('起始日期必须小于等于结束日期');
            return;
        }

        var time = $('#pushTime').val()
        if (!time.match(/^[0-9]{2}:[0-9]{2}:[0-9]{2}$/))
        {
            alert('推送时间的格式有误');
            return;
        }

        var id = $('#save_id').val();
        var url = '/taskManage/update/' + id;
        $.ajax({
            url:url,
            type:'PUT',
            data: {
                'jobId':$('#jobId').val(),
                'pushTime':$('#pushTime').val(),
                'beginDate':$('#beginDate').val(),
                'endDate':$('#endDate').val(),
                'command':$('#command').val(),
                'description':$('#description').val()
            },
            success:function (rep) {
                //刷新页面
                window.location.reload();
            }
        })
    })

    //修改按钮绑定事件
    $(".change-bic-button").click(function () {
        var id = $(this).attr('data-id')
        clearModal();
        $('#create-or-change').html("修改");

        var url = '/taskManage/getInfo/' + id;
        $.ajax({
            url:url,
            type:'GET',
            success:function (data) {
                $('#save_id').val(data._id);
                $('#jobId').val(data.jobId);
                $('#pushTime').val(data.pushTime);
                $('#beginDate').val(data.beginDate);
                $('#endDate').val(data.endDate);
                $('#command').val(data.command);
                $('#description').val(data.description);
                $('#createBicBt').css('display', 'none');
                $('#updateBicBt').css('display', 'block');
            }
        })
    });

    //创建按钮绑定事件
    $("#create-Manage-Bt").click(function () {
        clearModal();
        $('#create-or-change').html("新建");
        $('#createBicBt').css('display', 'block');
        $('#updateBicBt').css('display', 'none');
    });

    //删除按钮绑定事件
    $(".delete-bic-button").click(function () {
        var id = $(this).attr('data-id');

        var isConfirmed = confirm("删除后会停止任务,确认删除这项任务吗?");
        var url = '/taskManage/delete/' + id;
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

    //初始化模态框
    function clearModal() {
        $('#jobId').val('');
        $('#pushTime').val('');
        $('#beginDate').val('');
        $('#endDate').val('');
        $('#command').val('');
        $('#description').val('');
    }

    //搜索按钮绑定事件
    $("#searchButton").click(function () {

        var searchText = $('#searchJobId').val();
        location.href = '/taskManage/taskShow/search?jobId=' + searchText;
    })

    //测试按钮绑定事件
    $(".push-test-button").click(function () {

        var id = $(this).attr('data-id');
        $("#sureTestBtn").attr('data-id',id);
    })

    //提交测试按钮绑定事件
    $("#sureTestBtn").click(function () {
        
        var id = $(this).attr('data-id');
        $.ajax({
            url:'/taskManage/pushTest/' + id,
            type:'POST',
            data: {
                "openid":$("#pushOpenId").val()
            },
            success:function (data) {
                window.location.reload();
            }

        })
    })
})
