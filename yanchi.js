$.getJSON("https://y0123456789.github.io/check-pallas/minified-v3.json", function (data) {
    let mobileconfigURLs = [];
    Object.entries(data).forEach(entry => {
        if (entry[0] != "_date") {
            let versions = entry[1];
            versions.forEach(minor_version => {
                if (!minor_version.mdm_only && minor_version.mdm_available) {
                    let url = "https://y0123456789.github.io/check-pallas/" + minor_version.name + ".mobileconfig";
                    mobileconfigURLs.push(url);
                }
            });
        }
    });
    // 将 mobileconfig 文件的 URL 导入 JSON
    data["mobileconfig_urls"] = mobileconfigURLs;
    // 将 JSON 导出到文件
    let jsonStr = JSON.stringify(data, null, 2);
    let blob = new Blob([jsonStr], { type: "application/json" });
    saveAs(blob, "minified-v3-with-mobileconfig-urls.json");
});
