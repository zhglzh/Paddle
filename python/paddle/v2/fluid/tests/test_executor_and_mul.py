#  Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserve.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
import unittest

import numpy
import paddle.v2.fluid.core as core

from paddle.v2.fluid.executor import Executor
from paddle.v2.fluid.layers import mul, data


class TestExecutor(unittest.TestCase):
    def test_mul(self):
        a = data(name='a', shape=[784], dtype='float32')
        b = data(
            name='b',
            shape=[784, 100],
            dtype='float32',
            append_batch_size=False)
        out = mul(x=a, y=b)
        place = core.CPUPlace()
        a_np = numpy.random.random((100, 784)).astype('float32')
        b_np = numpy.random.random((784, 100)).astype('float32')
        exe = Executor(place)
        outs = exe.run(feed={'a': a_np, 'b': b_np}, fetch_list=[out])
        out = outs[0]
        self.assertEqual((100, 100), out.shape)
        self.assertTrue(numpy.allclose(out, numpy.dot(a_np, b_np)))


if __name__ == '__main__':
    unittest.main()
