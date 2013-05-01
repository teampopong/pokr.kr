try {
    var rawdata = document.getElementById('person-data').text,
        data = JSON.parse(rawdata),
        events = PG.data.People(data),
        graph = PG.graph.Timeline('#timeline', 720, 100);
    graph.render(events);
} catch (e) {
    // do nothing
}
