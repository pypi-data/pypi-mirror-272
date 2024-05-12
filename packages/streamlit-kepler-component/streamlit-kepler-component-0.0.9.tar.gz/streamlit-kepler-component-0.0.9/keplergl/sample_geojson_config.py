sampleGeojsonConfig = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [
                {
                    "dataId": ["bart-stops-geo-2"],
                    "id": "2ua7g6t8",
                    "name": ["exits"],
                    "type": "range",
                    "value": [6121, 13547],
                    "plotType": {"type": "histogram"},
                    "animationWindow": "free",
                    "yAxis": None,
                    "view": "side",
                    "speed": 1,
                    "enabled": True
                },
                {
                    "dataId": ["sf-zip-geo"],
                    "id": "kt1fkkbrb",
                    "name": ["ZIP_CODE"],
                    "type": "range",
                    "value": [94103, 94133],
                    "plotType": {"type": "histogram"},
                    "animationWindow": "free",
                    "yAxis": None,
                    "view": "side",
                    "speed": 1,
                    "enabled": True
                }
            ],
            "layers": [
                {
                    "id": "ze2p6id",
                    "type": "geojson",
                    "config": {
                        "dataId": "bart-stops-geo",
                        "label": "Bart Stops Geo",
                        "color": [151, 14, 45],
                        "columns": {"geojson": "_geojson"},
                        "isVisible": True,
                        "visConfig": {
                            "opacity": 0.8,
                            "thickness": 0.5,
                            "strokeColor": [77, 193, 156],
                            "colorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": ["#5A1846",
                                           "#900C3F",
                                           "#C70039",
                                           "#E3611C",
                                           "#F1920E",
                                           "#FFC300"]},
                            "strokeColorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": [
                                    "#5A1846",
                                    "#900C3F",
                                    "#C70039",
                                    "#E3611C",
                                    "#F1920E",
                                    "#FFC300"]},
                            "radius": 22.5,
                            "sizeRange": [0, 10],
                            "radiusRange": [0, 50],
                            "heightRange": [0, 500],
                            "elevationScale": 5,
                            "stroked": True,
                            "filled": True,
                            "enable3d": False,
                            "wireframe": False
                        },
                        "textLabel": [
                            {
                                "field": None,
                                "color": [255, 255, 255],
                                "size": 18,
                                "offset": [0, 0],
                                "anchor": "start",
                                "alignment": "center"
                            }
                        ]
                    },
                    "visualChannels": {
                        "colorField": None,
                        "colorScale": "quantile",
                        "sizeField": None,
                        "sizeScale": "linear",
                        "strokeColorField": None,
                        "strokeColorScale": "quantile",
                        "heightField": None,
                        "heightScale": "linear",
                        "radiusField": None,
                        "radiusScale": "linear"
                    }
                },
                {
                    "id": "ho3fgt9",
                    "type": "geojson",
                    "config": {
                        "dataId": "sf-zip-geo",
                        "label": "SF Zip Geo",
                        "color": [136, 87, 44],
                        "columns": {
                            "geojson": "_geojson"
                        },
                        "isVisible": True,
                        "visConfig": {
                            "opacity": 0.8,
                            "thickness": 0.5,
                            "strokeColor": [255,
                                            254,
                                            213],
                            "colorRange": {
                                "name": "UberPool 8",
                                "type": "diverging",
                                "category": "Uber",
                                "colors": [
                                    "#213E9A",
                                    "#3C1FA7",
                                    "#811CB5",
                                    "#C318B0",
                                    "#D01367",
                                    "#DE0F0E",
                                    "#EC7007",
                                    "#F9E200"],
                                "reversed": False
                            },
                            "strokeColorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": [
                                    "#5A1846",
                                    "#900C3F",
                                    "#C70039",
                                    "#E3611C",
                                    "#F1920E",
                                    "#FFC300"]},
                            "radius": 10,
                            "sizeRange": [0, 10],
                            "radiusRange": [0,
                                            50],
                            "heightRange": [0,
                                            500],
                            "elevationScale": 5,
                            "stroked": True,
                            "filled": True,
                            "enable3d": False,
                            "wireframe": False},
                        "textLabel": [
                            {"field": None,
                             "color": [255, 255,
                                       255],
                             "size": 18,
                             "offset": [0, 0],
                             "anchor": "start",
                             "alignment": "center"}]},
                    "visualChannels": {
                        "colorField": {"name": "ID",
                                       "type": "integer"},
                        "colorScale": "quantile",
                        "sizeField": None,
                        "sizeScale": "linear",
                        "strokeColorField": None,
                        "strokeColorScale": "quantile",
                        "heightField": None,
                        "heightScale": "linear",
                        "radiusField": None,
                        "radiusScale": "linear"}}],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "bart-stops-geo": ["name"],
                        "sf-zip-geo": ["OBJECTID",
                                       "ZIP_CODE", "ID",
                                       "name",
                                       "STREETNAME"]
                    },
                    "enabled": True
                },
                "brush": {
                    "size": 0.5,
                    "enabled": False},
                "geocoder": {"enabled": False}
            },
            "layerBlending": "normal"
        }
    }
}
