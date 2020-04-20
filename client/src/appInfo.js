const modelInfo = {
    modelCategories: [
        {
            label: "people-close-up",
            description: "close up shot of people"
        },
        {
            label: "people-landscape",
            description: "people in foreground, landscape in background"
        },
        {
            label: "landscape",
            description: "landscape shot"
        }
    ]
}

const appInfo = {
    appName: "Star Wars Explorer",
    showcase: {
        items: [
            {
                url: "https://cdn.tourradar.com/s3/review/750x400/136555_2e8b6dfb.jpg",
                category: modelInfo.modelCategories[0].label
            },
            {
                url: "https://cdn.tourradar.com/s3/review/750x400/133738_4485aa24.jpg",
                category: modelInfo.modelCategories[1].label
            },
            {
                url: "https://cdn.tourradar.com/s3/review/750x400/98778_bacc2c2d.jpg",
                category: modelInfo.modelCategories[2].label
            },

        ]
    },
    submitFormPlaceholderUrl: "https://cdn.tourradar.com/s3/review/750x400/98778_bacc2c2d.jpg"
}

export { appInfo, modelInfo };