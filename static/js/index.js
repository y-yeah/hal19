let count = 0;
window.onload = () => {
  const capturePic = () => {
    const photo = document.getElementById("photo");
    axios
      .get("/photo", {
        crossorigin: true,
        headers: {
          "Access-Control-ALlow-Origin": "*"
        }
      })
      .then(res => {
        axios
          .get("/photo/date", {
            crossorigin: true,
            headers: {
              "Access-Control-ALlow-Origin": "*"
            }
          })
          .then(nowRes => {
            const arrayBufferToBase64 = buffer => {
              let binary = "";
              let bytes = new Uint8Array(buffer);
              for (let i = 0; i < bytes.byteLength; i++) {
                binary += String.fromCharCode(bytes[i]);
              }
              return window.btoa(binary);
            };

            for (let i = count; i < res.data.length; i++, count++) {
              const hvrbox = document.createElement("div");
              const hvrbox_layer_top = document.createElement("div");
              const hvrbox_text = document.createElement("a");
              let nowString = "";

              hvrbox.className = "hvrbox";
              hvrbox_layer_top.className = "hvrbox_layer_top";
              hvrbox_text.className = "hvrtxt";

              hvrbox.setAttribute(
                "style",
                `background-image: url("data:image/jpg;base64, ${arrayBufferToBase64(
                  res.data[i]
                )}")`
              );

              nowRes.data[i].forEach(char => {
                if (char !== ",") {
                  nowString += char;
                }
              });
              hvrbox_text.innerText = nowString;

              hvrbox_layer_top.appendChild(hvrbox_text);
              hvrbox.appendChild(hvrbox_layer_top);
              photo.appendChild(hvrbox);
            }

            document.getElementById("dscr").innerText =
              res.data.length + " faces have been detected.";
          })
          .catch(err => {
            console.err(err);
          });
      })
      .catch(err => {
        console.err(err);
      });
  };
  setInterval(capturePic, 10);
};
