#include <gmock/gmock.h>
#include <gtest/gtest.h>

class Mock
{
public:
	MOCK_METHOD0(foo, void());
};

class MockTest: public ::testing::Test
{
protected:
	Mock mock;
};

TEST(conan, simple_test)
{
	int a = 1 + 1;
	EXPECT_EQ(a, 2);
}

TEST_F(MockTest, simple_mock)
{
	EXPECT_CALL(mock, foo())
		.Times(1);
		
	mock.foo();
}