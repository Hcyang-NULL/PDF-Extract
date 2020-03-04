

$(document).ready(function () {
    $("body").on("change", "#inputGroupFile03", function (e) {
        let pdf_name = e.target.value;
        pdf_name = pdf_name.split('\\');
        pdf_name = pdf_name[pdf_name.length - 1];
        $("#label-file").text(pdf_name);
        let pdf_suffix = pdf_name.split('.');
        pdf_suffix = pdf_suffix[pdf_suffix.length - 1];
        console.log(pdf_suffix);
        if(pdf_suffix !== 'pdf') {
            alert("仅支持导入pdf文件");
            return
        }
        else {
            $("#choose").submit();
        }
    });

    $(".navbar").click(function () {
        window.location.href = 'http://39.106.57.52'
    })

});