from typing import Collection, Union, Sequence, Optional

from geometry_msgs.msg import Vector3, Point
from rclpy.clock import Clock
from std_msgs.msg import ColorRGBA, Header
from visualization_msgs.msg import Marker

from path_score.helpers import Position


def get_marker(clock: Clock,

               path_id: int,
               path: Collection[Union[Sequence[float], Position]],

               weights: Optional[Collection[float]] = None,
               weight_max: Optional[float] = 1.0,

               frame_id: Optional[str] = "/map",
               ns: Optional[str] = "paths",
               scale: Optional[float] = 0.01,

               color=ColorRGBA(r=0.0, g=0.0, b=1.0, a=1.0)
               ) -> Marker:
    """
    Generates a visualization_msgs::msg::Marker from a set of points
    Can colorize points on a scale based on another set of values ('weights')
    """
    # Use point cloud instead?
    m = Marker(
        header=Header(frame_id=frame_id, stamp=clock.now().to_msg()),
        ns=ns,
        action=Marker.ADD,
        id=path_id,
        type=Marker.POINTS,
        scale=Vector3(x=scale, y=scale),
        color=color
    )

    m.points.extend(Point(x=1.0 * pt[0], y=1.0 * pt[1]) for pt in path)
    if weights is not None:
        assert len(path) == len(weights)
        m.colors.extend(
            # TODO: Better color range generation
            ColorRGBA(r=1.0, g=1.0 - min(max(1.0 * wt / weight_max, 0.0), 1.0), b=0.0, a=1.0) for wt in weights
        )

    return m
