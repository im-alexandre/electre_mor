        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        var csrftoken = getCookie('csrftoken');
        
        $(document).ready(function() {
            $('.edit').editable('{% url "editardados" %}', {
                // type: 'POST',
                id: 'tipoId',
                name: 'nome',
                submit : 'Salvar',
                cancel : 'Cancelar',
                cancelcssclass : 'btn btn-danger',
                submitcssclass : 'btn btn-success',
                tooltip   : 'Clique para editar o nome',
                ajaxoptions: {
                    'beforeSend': function(xhr) {
                        xhr.setRequestHeader('X-CSRFToken', csrftoken);
                    },
                }
            }
            );
        });
        function funcao() {
            $('[data-toggle="tooltip"]').tooltip()
        }
funcao();
