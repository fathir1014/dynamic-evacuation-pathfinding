def calculate_risk(node):
    return (
        0.4 * node.smoke +
        0.3 * node.debris +
        0.2 * node.liquid +
        0.1 * node.crowd
    )


def calculate_health_damage(node):
    return (
        1.4 * node.smoke +
        2.0 * node.debris +
        1.2 * node.liquid +
        0.8 * node.crowd
    )