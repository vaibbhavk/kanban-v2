pur = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style type="text/css">
        @page {
            @top-left {
                background: #82b965;
                content: counter(page);
                height: 1cm;
                text-align: center;
                width: 1cm;
            }

            @top-center {
                background: #82b965;
                content: '';
                display: block;
                height: .05cm;
                opacity: .5;
                width: 100%;
            }

            @top-right {
                content: string(heading);
                font-size: 9pt;
                height: 1cm;
                vertical-align: middle;
                width: 100%;
            }
        }

        @page: first {
            background-size: cover;
            margin: 0;
        }

        @page chapter {
            background: #82b965;
            margin: 0;

            @top-left {
                content: none;
            }

            @top-center {
                content: none;
            }

            @top-right {
                content: none;
            }
        }

        html {
            color: #393939;
            font-family: "Noto sans", sans-serif;
            font-size: 11pt;
            font-weight: 300;
            line-height: 1.5;
        }

        h1 {
            color: #82b965;
            font-size: 38pt;
            margin: 5cm, 2cm, 0, 2cm;
            page: no-chapter;
            width: 100%;
        }

        h2,
        h3,
        h4 {
            color: black;
            font-weight: 400;
        }

        h2 {
            break-before: always;
            font-size: 28pt;
            string-set: heading content();
        }

        h3 {
            font-weight: 300;
            font-size: 15pt;
        }

        h4 {
            font-size: 13pt;
        }

        #cover {
            align-content: space-between;
            display: flex;
            flex-wrap: wrap;
            height: 297mm;
        }

        #cover footer {
            background: #82b965;
            flex: 1 50%;
            margin: 0 -2cm;
            padding: 1cm 0;
            padding-left: 3cm;
        }

        #contents {
            break-after: left;
        }

        #contents h2 {
            font-size: 20pt;
            font-weight: 400;
            margin-bottom: 3cm;
        }

        #contents h3 {
            font-weight: 500;
            margin: 3em 0 1em;
        }

        #contents h3::before {
            background: #82b965;
            content: '';
            display: block;
            height: .08cm;
            margin-bottom: .25cm;
            width: 2cm;
        }

        #contents ul {
            list-style: none;
            padding-left: 0;
        }

        #contents ul li {
            border-top: .25pt solid #c1c1c1;
            margin: .25cm 0;
            padding-top: .25cm;
        }

        #contents ul li::before {
            color: #82b965;
            content: '* ';
            font-size: 40pt;
            line-height: 16pt;
            vertical-align: bottom;
        }

        #contents ul li a {
            color: inherit;
            text-decoration-line: inherit;
        }
    </style>
</head>

<body>
    <article id="cover">
         <h1>{{data["username"]}}</h1> 
        <footer>
          {{data["email"]}}
        </footer>
    </article>
    <article id="contents">
        <h2>Monthly Progress Report (Kanban V2)</h2>
        <ul>
        <li>Total tasks assigned: {{data["total"]}}</li>
        <li>Total tasks completed: {{data["total_completed"]}}</li>
        </ul>
    </article>
</body>

</html>
'''
