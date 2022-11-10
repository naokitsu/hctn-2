html_template = """
<head>
    <style>
    .tab {{
        overflow: hidden;
        border: 1px solid #ccc;
        background-color: #f1f1f1;}}
    .tab button {{
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 8px 8px;
            transition: 0.3s;
        }}
        .tab button:hover {{
            background-color: #ddd;
        }}
        .tab button.active {{
            background-color: #ccc;
        }}
        .tabcontent {{
            display: none;
            border: 1px solid #ccc;
        }}
    </style>
    <meta charset="UTF-8">
<body style="padding: 10px">
<div class="tab">
    <button class="groupLinks" id="defaultOpen" onclick="openGroup(event, 'Positive')">Файлы влияющие на цвет заголовка</button>
    <button class="groupLinks" onclick="openGroup(event, 'Negative')">Файлы не влияющие на цвет заголовка</button>
</div>
<div id="Positive" class="group">
    <div class="tab">
        {}
    </div>
</div>
<div id="Negative" class="group">
    <div class="tab">
        {}
    </div>
</div>
{}
<script>
    function openGroup(evt, groupName) {{
        var i, content, buttons;
        content = document.getElementsByClassName("group");
        for (i = 0; i < content.length; i++) {{
            content[i].style.display = "none";
        }}
        buttons = document.getElementsByClassName("groupLinks");
        for (i = 0; i < buttons.length; i++) {{
            buttons[i].className = buttons[i].className.replace(" active", "");
        }}
        document.getElementById(groupName).style.display = "block";
        evt.currentTarget.className += " active";
    }}
    function openEntry(evt, entryName) {{
        var i, content, buttons;
        content = document.getElementsByClassName("entry");
        for (i = 0; i < content.length; i++) {{
            content[i].style.display = "none";
        }}
        buttons = document.getElementsByClassName("entryLinks");
        for (i = 0; i < buttons.length; i++) {{
            buttons[i].className = buttons[i].className.replace(" active", "");
        }}
        document.getElementById(entryName).style.display = "block";
        evt.currentTarget.className += " active";
    }}
</script>
<script>
    document.getElementById("defaultOpen").click();
</script>
</body>
</html>
"""

header_template = """
<h2>Заголовок {}</h2>
<p>Тег "color": <tagname style="color:green">совпадает</tagname> (Эталон: rgb(0, 0, 0))</p><p>Сравнение скриншотов: <tagname style="color:green">совпадают</tagname></p><div style="border: 1px solid #ccc"><img src="./images/7fc365ec-e5ec-4385-84c8-835f29c12993/489152de-4b61-4919-99bd-07d33e01580e.png"><br><img src="./images/without-styles/489152de-4b61-4919-99bd-07d33e01580e.png"></div>
"""