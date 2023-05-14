$.getJSON("https://y0123456789.github.io/check-pallas/minified-v3.json", function (data) {
    Object.entries(data).forEach(entry => {
        if (entry[0] == "_date") {
            $(".last_updated").text("最后更新: " + new Date(entry[1]).toLocaleString());
        } else {
            let [title, versions] = entry;
            
            let thead = $("<th>");
            thead.attr("colspan", 4);
            thead.append("<strong>" + title + "</strong>")
            $(".builds_viewcontainer").append(thead);

            versions.forEach(minor_version => {
                let trow = $("<tr>");
                let tversion = $("<td>");
                tversion.text(minor_version.name);

                if (minor_version.alternate) {
                    spanalternate = $("<span>");
                    spanalternate.attr("style", "font-size: 14px");
                    spanalternate.text("Alternate - iOS/iPadOS 14.5+ required");
                    tversion.append($("<br>"))
                    tversion.append(spanalternate);
                }

                // If latest: texpiry is longest span

                let texpiry = $("<td>");
                if (minor_version.latest){ 
                    texpiry.attr("colspan", 3);
                    texpiry.text("Latest available");
                } else if (!minor_version.date) {
                    texpiry.attr("colspan", 1);
                    texpiry.text("最新版本");
                } else {
                    texpiry.text(new Date(Date.parse(minor_version.date)).toLocaleString())
                    if (minor_version.imminent) {
                        texpiry.text(`即将过期 (过期时间 ${texpiry.text()})`)
                        texpiry.css("color", "red");
                    }
                }

                let tdownload = $("<td>")
                if (minor_version.mdm_only) {
                    tdownload.text("仅限MDM")
                } else {
                    let tdownloadlink = $("<a>")
                    tdownloadlink.attr("href", "#")
                    
                   // 定义两个日期字符串
                   const date1Str = new Date(Date.parse(minor_version.date)).toLocaleString();
                   const date2Str = new Date().toLocaleString();
                   // 将日期字符串转换为日期对象
                   const date1 = new Date(date1Str);
                   const date2 = new Date(date2Str);
                   // 计算两个日期之间的时间差，单位为毫秒
                   const diffMs = date1.getTime() - date2.getTime();
                   // 将毫秒转换为日、时、分
                   const diffSec = diffMs / 1000;
                   const diffMin = diffMs / (1000 * 60);
                   const diffHours = diffMs / (1000 * 60 * 60);
                   const diffDays = diffMs / (1000 * 60 * 60 * 24);
                   // 格式化时间差为 日 时 分
                   const days = Math.floor(diffDays);
                   const hours = Math.floor(diffHours - (days * 24));
                   const minutes = Math.floor(diffMin - (days * 24 * 60) - (hours * 60));
                   const seconds = Math.floor(diffSec - (days * 24 * 60 * 60) - (hours * 60 * 60) - (minutes * 60));
                   const formattedDiff = `${days}天${hours}时${minutes}分${seconds}秒`;
                   // 输出格式化后的时间差
                   tdownloadlink.text(`下载描述文件 剩余(${formattedDiff})`)
                   tdownloadlink.click(function () {
                   // 当用户点击下载链接时，使用指定的模板来创建配置文件，并将其保存为 mobileconfig 格式的文件
                   $.get("https://dhinakg.github.io/check-pallas/template.mobileconfig", function (response) {
                   console.log(title)
                   console.log(minor_version)
                   let filename = `${minor_version.name} —剩余${days}天.mobileconfig`;
                   let blob = new Blob([response.replace(/\{DELAYPERIOD\}/g, minor_version.delay.toString())], { type: "application/x-apple-aspen-config" })
                   saveAs(blob, filename)
                   })
                        return false;
                    })
                    tdownload.append(tdownloadlink)
                }
                let tnotavailable = $("<td>");
                if (!minor_version.mdm_available) {
                    tnotavailable.text("Not available with MDM")
                    texpiry.attr("colspan", Math.min(texpiry.attr("colspan"), 2));
                } else {
                    tdownload.attr("colspan", 2);
                }

                trow.append(tversion)
                trow.append(texpiry)

                if (!minor_version.latest) {
                    trow.append(tdownload);
                }

                if (!minor_version.mdm_available) {
                    trow.append(tnotavailable);
                }

                $(".builds_viewcontainer").append(trow);
            });
        }
    });

})
