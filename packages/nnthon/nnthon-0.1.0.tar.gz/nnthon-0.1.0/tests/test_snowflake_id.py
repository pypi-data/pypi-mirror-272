from nnthon import SnowFlakeID


def test_snowflake_id():
    worker1 = SnowFlakeID(1)
    worker2 = SnowFlakeID(2)
    w1_id = worker1.new_id()
    w2_id = worker2.new_id()
    assert w2_id > w1_id
