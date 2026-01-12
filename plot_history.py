import marimo

__generated_with = "0.18.4"
app = marimo.App(width="columns")


@app.cell(column=0)
def _():
    import plotly.express as px
    import pandas as pd
    import plotly.figure_factory as ff
    from datetime import datetime
    import copy

    try:
        from details import life_details
    except ModuleNotFoundError:
        """
        Fake data - I ain't gonna upload all my personal information online.... 
        """
        print("@Ian Check Obsidian Vault - phd_viz")
        life_details = pd.DataFrame([
            # Moves
            dict(Event="Moved to X", Start="2015-01-10", Finish="2015-01-20", Resource="Move"),
            dict(Event="Moved to Y.", Start="2018-05-10", Finish="2018-05-20", Resource="Move"),
            # Education
            dict(Event="B.Sc at UoA", Start="2013-09-01", Finish="2015-05-09", Resource="Education"),
            dict(Event="M.Sc at UoB", Start="2016-09-17", Finish="2021-01-15", Resource="Education"),
            # Work/Research Experience
            dict(Event="Worked in Tech", Start="2017-05-09", Finish="2023-07-30", Resource="Work"),
        ])
    return datetime, ff, life_details, pd, px


@app.cell
def _(life_details, pd, px):
    def plot_timeline_grouped_resource(events: pd.DataFrame):
        fig = px.timeline(
            events, x_start="Start", x_end="Finish", y="Resource", color="Resource", text="Event", opacity=0.8
        )
        # fig.update_yaxes()#autorange="reversed",) # otherwise tasks are listed from the bottom up
        # fig.update_xaxes(col=[])
        fig.update_layout(
            yaxis_title=None,
            yaxis=dict(
                tickfont=dict(size=20),
            ),
            xaxis=dict(tickfont=dict(size=15), showline=False, showdividers=False, showgrid=False, showspikes=False),
        )
        fig.update_traces(insidetextfont=dict(color="black", size=20, family="Times New Roman"))
        fig.update_traces(outsidetextfont=dict(color="black", size=20, family="Times New Roman"))
        fig.write_image("plots/personal.png", scale=2)
        fig.show()

    plot_timeline_grouped_resource(events=life_details)
    return


@app.cell
def _(datetime, ff, pd):
    try:
        from details import research_projects
    except (ModuleNotFoundError, ImportError):
        """
        Fake data - I ain't gonna upload all my personal information online.... 
        """
        print("@Ian Check Obsidian Vault - phd_viz")
        research_projects = pd.DataFrame([
            # Moves
            dict(Task="Neuroscience", Start="2023-09-15", Finish="2025-01-12", Resource="Neuroscience Project 1"),
            dict(Task="Neuroscience", Start="2025-03-23", Finish="2025-07-12", Resource="Neuroscience Project 2"),
            dict(Task="ML", Start="2025-07-12", Finish="2026-01-14", Resource="Project Name"),
        ])

    def plot_timeline_grouped_project(events: list[dict[str, str]]):
        OFFSET_CONSTANT = 2  # Not a damn clue why I have to do this
        annots = []
        tracked_tasks = {}
        for i, event in enumerate(events):
            if event["Task"] not in tracked_tasks:
                tracked_tasks[event["Task"]] = len(events) - len(tracked_tasks) - OFFSET_CONSTANT
                y_idx = tracked_tasks[event["Task"]]
            else:
                y_idx = tracked_tasks[event["Task"]]

            start = datetime.strptime(event["Start"], "%Y-%m-%d")
            end = datetime.strptime(event["Finish"], "%Y-%m-%d")
            midpoint = start.date() + (end - start) / 2
            annots.append(dict(x=midpoint, y=y_idx, text=event["Resource"], showarrow=False, font=dict(color="black")))

        fig = ff.create_gantt(
            events,
            index_col="Resource",
            show_colorbar=True,
            group_tasks=True,
            title="Research Projects",
            show_hover_fill=True,
        )

        new_data = []
        for el in fig["data"]:
            el["showlegend"] = False
            new_data.append(el)
        fig["data"] = new_data

        fig["layout"]["annotations"] = annots
        fig["layout"]["yaxis"]["autorange"] = True
        fig["layout"]["height"] = 800
        fig["layout"]["width"] = 1_500
        # print(fig)
        fig.write_image("plots/projects.png", scale=5)
        # fig.show()

    plot_timeline_grouped_project(events=research_projects)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell(column=1)
def _():
    return


if __name__ == "__main__":
    app.run()
