var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

today = yyyy + '-' + mm + '-' + dd;
$("#date").val(today);

Dropzone.autoDiscover = false;
window.onload = function() {
    const editor = new EditorJS({
        /**
         * Id of Element that should contain Editor instance
         */
        holder: 'editorjs',
        placeholder: 'Напишите новость!',
        tools: {
            header: {
                class: Header,
                inlineToolbar: true
            },
            list: {
                class: List,
                inlineToolbar: true
            }
        }
    });

    var dzOptions = {
        url: window.location.pathname,
        dictDefaultMessage: "Перетащите файлы сюда или нажмите для загрузки через Проводник.",
        clickable: true,
        uploadMultiple: true,
        addRemoveLinks: true,
        acceptedFiles: "image/*",
        autoProcessQueue: false,
        parallelUploads: 10,
        init: function () {
            var myDropzone = this;
            var outputData = null;

            $("#save").click(async function (e) {
                e.preventDefault();


                outputData = await editor.save().then((outputData) => {
                    return outputData;
                });

                if (myDropzone.files.length > 0) {
                    myDropzone.processQueue();
                } else {
                    console.log('manual!');
                    // send an ajax by hand if no files loaded
                    var formData = new FormData();
                    formData.append('text', JSON.stringify(outputData.blocks));
                    formData.append('date', $("#date").val());
                    $.ajax({
                        method: "POST",
                        url: window.location.pathname,
                        data: formData,
                        processData: false,
                        contentType: false,
                        beforeSend: function( xhr ) {
                            $("#loader").html("Загружаем...");
                        },
                        success: function(msg) {
                            $("#loader").html("Загружено!");
                            setTimeout(function () {
                                $("#loader").html("");
                            }, 2000)
                        },
                        error: function() {
                            $("#loader").html("Упс, что-то пошло не так!");
                        }
                    });
                }
            });

            this.on('sendingmultiple', function(file, xhr, formData) {
                formData.append('text', JSON.stringify(outputData.blocks));
                formData.append('date', $("#date").val());
            });

            this.on('sending', function(file, xhr, formData) {
                formData.append('text', JSON.stringify(outputData.blocks));
                formData.append('date', $("#date").val());
            });

            this.on("complete", function() {
                $("#loader").html("Загружено!");
                setTimeout(function () {
                    myDropzone.removeAllFiles();
                    $("#loader").html("");
                }, 2000); // <3 JS
            });
        }
    };

    var uploader = document.querySelector('#drop');
    var newDropzone = new Dropzone(uploader, dzOptions);
};
