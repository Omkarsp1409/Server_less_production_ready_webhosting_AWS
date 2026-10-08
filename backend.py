const MONITORING_API =
    "https://ggc5qhlm39.execute-api.us-east-1.amazonaws.com/deploy/monitoring";


// --------------------------------------------------
// UPDATE TEXT
// --------------------------------------------------

function setText(id, value) {

    const element = document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}


// --------------------------------------------------
// UPDATE STATUS
// --------------------------------------------------

function setStatus(id, text, healthy = true) {

    const element = document.getElementById(id);

    if (!element) {
        return;
    }

    element.textContent = `● ${text}`;

    element.dataset.state =
        healthy ? "healthy" : "error";
}


// --------------------------------------------------
// GET CURRENT TIME
// --------------------------------------------------

function currentTime() {

    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

}


// --------------------------------------------------
// MAIN MONITORING FUNCTION
// --------------------------------------------------

async function checkStatus() {

    console.log("Checking AWS infrastructure...");


    // Initial state

    setStatus(
        "apiStatus",
        "Checking...",
        true
    );

    setStatus(
        "ec2Status",
        "Checking...",
        true
    );

    setText(
        "cpuUsage",
        "--"
    );

    setText(
        "cpuInfo",
        "Checking..."
    );

    setText(
        "instanceInfo",
        "Instance: Checking..."
    );


    try {

        // --------------------------------------------------
        // CALL API GATEWAY
        // --------------------------------------------------

        const response = await fetch(
            MONITORING_API,
            {
                method: "GET",
                cache: "no-store"
            }
        );


        // --------------------------------------------------
        // CHECK HTTP RESPONSE
        // --------------------------------------------------

        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );

        }


        // --------------------------------------------------
        // CONVERT RESPONSE TO JSON
        // --------------------------------------------------

        const data =
            await response.json();


        console.log(
            "Monitoring Data:",
            data
        );


        // --------------------------------------------------
        // API STATUS
        // --------------------------------------------------

        setStatus(
            "apiStatus",
            "Healthy",
            true
        );


        // --------------------------------------------------
        // CHECK EC2 INSTANCES
        // --------------------------------------------------

        if (
            !data.instances ||
            data.instances.length === 0
        ) {

            setStatus(
                "ec2Status",
                "No Instances",
                false
            );

            setText(
                "instanceInfo",
                "No EC2 instances found"
            );

            setText(
                "cpuUsage",
                "--"
            );

            setText(
                "cpuInfo",
                "No metric available"
            );

        }

        else {

            // Get first EC2 instance

            const instance =
                data.instances[0];


            // --------------------------------------------------
            // EC2 STATE
            // --------------------------------------------------

            const state =
                instance.state || "unknown";


            const formattedState =
                state.charAt(0).toUpperCase()
                + state.slice(1);


            setStatus(
                "ec2Status",
                formattedState,
                state === "running"
            );


            // --------------------------------------------------
            // INSTANCE ID
            // --------------------------------------------------

            setText(
                "instanceInfo",
                `Instance: ${
                    instance.instance_id || "N/A"
                }`
            );


            // --------------------------------------------------
            // CPU UTILIZATION
            // --------------------------------------------------

            if (
                typeof instance.cpu_utilization
                === "number"
            ) {

                const cpu =
                    instance.cpu_utilization;


                setText(
                    "cpuUsage",
                    `${cpu.toFixed(2)}%`
                );


                if (cpu < 80) {

                    setText(
                        "cpuInfo",
                        "Normal"
                    );

                }

                else {

                    setText(
                        "cpuInfo",
                        "High"
                    );

                }

            }

            else {

                setText(
                    "cpuUsage",
                    "--"
                );

                setText(
                    "cpuInfo",
                    "No recent metric"
                );

            }

        }


        // --------------------------------------------------
        // SYSTEM ACTIVITY
        // --------------------------------------------------

        const time =
            currentTime();


        setText(
            "activityTime1",
            time
        );


        setText(
            "activity1",
            `EC2 monitoring check completed (${
                data.total_instances ?? 0
            } instance(s))`
        );


        setText(
            "activityTime2",
            time
        );


        setText(
            "activity2",
            "API Gateway request received"
        );


        setText(
            "activityTime3",
            time
        );


        setText(
            "activity3",
            "Lambda monitoring response received"
        );


        // --------------------------------------------------
        // LAST UPDATED MESSAGE
        // --------------------------------------------------

        setText(
            "message",
            `Last updated: ${time} | Region: ${
                data.region || "N/A"
            }`
        );


    }


    // --------------------------------------------------
    // ERROR HANDLING
    // --------------------------------------------------

    catch (error) {

        console.error(
            "Monitoring API Error:",
            error
        );


        setStatus(
            "apiStatus",
            "Unavailable",
            false
        );


        setStatus(
            "ec2Status",
            "Unavailable",
            false
        );


        setText(
            "cpuUsage",
            "--"
        );


        setText(
            "cpuInfo",
            "Monitoring API unavailable"
        );


        setText(
            "instanceInfo",
            "Unable to retrieve instance data"
        );


        setText(
            "activityTime1",
            currentTime()
        );


        setText(
            "activity1",
            "EC2 monitoring request failed"
        );


        setText(
            "activity2",
            "API Gateway/Lambda request failed"
        );


        setText(
            "message",
            `Monitoring error: ${error.message}`
        );

    }

}


// --------------------------------------------------
// RUN WHEN PAGE LOADS
// --------------------------------------------------

document.addEventListener(
    "DOMContentLoaded",
    checkStatus
);


// --------------------------------------------------
// AUTO REFRESH EVERY 60 SECONDS
// --------------------------------------------------

setInterval(
    checkStatus,
    60000
);
