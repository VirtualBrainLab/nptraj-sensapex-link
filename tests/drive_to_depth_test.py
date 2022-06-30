from unittest import TestCase
from unittest.mock import Mock
# noinspection PyPackageRequirements
import socketio


# noinspection DuplicatedCode
class DriveToDepthTest(TestCase):
    """Tests drive to depth event"""
    DRIVE_SPEED = 5000

    def setUp(self) -> None:
        """Setup test case"""
        self.sio = socketio.Client()
        self.mock = Mock()

        self.sio.connect('http://localhost:8080')

    def test_move_no_asserts(self):
        """Test movement without asserts"""
        self.sio.emit('register_manipulator', 1)
        self.sio.emit('register_manipulator', 2)
        self.sio.emit('bypass_calibration', 1)
        self.sio.emit('bypass_calibration', 2)

        self.sio.emit('drive_to_depth',
                      {'manipulator_id': 1, 'depth': 0,
                       'speed': self.DRIVE_SPEED},
                      callback=self.mock)
        self.sio.emit('drive_to_depth',
                      {'manipulator_id': 2, 'depth': 0,
                       'speed': self.DRIVE_SPEED},
                      callback=self.mock)

        self.sio.emit('drive_to_depth',
                      {'manipulator_id': 1, 'depth': 10000,
                       'speed': self.DRIVE_SPEED},
                      callback=self.mock)
        self.sio.emit('drive_to_depth',
                      {'manipulator_id': 2, 'depth': 10000,
                       'speed': self.DRIVE_SPEED},
                      callback=self.mock)

        while self.mock.call_count != 4:
            pass

    def test_move_with_asserts(self):
        """Test movement with asserts"""
        self.sio.emit('register_manipulator', 1)
        self.sio.emit('register_manipulator', 2)
        self.sio.emit('bypass_calibration', 1)
        self.sio.emit('bypass_calibration', 2)

        self.sio.emit('drive_to_depth',
                      {'manipulator_id': 1, 'depth': 0,
                       'speed': self.DRIVE_SPEED},
                      callback=self.mock)
        self.wait_for_callback()
        args = self.mock.call_args.args
        self.assertEqual(args[0], 1)
        self.assertLess(abs(args[1]), 1)
        self.assertEqual(args[2], '')

        self.sio.emit('drive_to_depth',
                      {'manipulator_id': 1, 'depth': 10000,
                       'speed': self.DRIVE_SPEED},
                      callback=self.mock)
        self.wait_for_callback()

    def test_move_unregistered(self):
        """Test movement with unregistered manipulator"""
        self.sio.emit('drive_to_depth',
                      {'manipulator_id': 1, 'depth': 0,
                       'speed': self.DRIVE_SPEED},
                      callback=self.mock)
        self.wait_for_callback()
        self.mock.assert_called_with(1, 0, 'Manipulator not registered')

    def tearDown(self) -> None:
        """Cleanup test case"""
        self.sio.disconnect()

    def wait_for_callback(self):
        """Wait for callback to be called"""
        while not self.mock.called:
            pass
        self.mock.called = False
