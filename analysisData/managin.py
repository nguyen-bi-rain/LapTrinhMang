def max_profit(N, K, profits):
    # Initialize the dp array
    dp = [0] * (N + 1)

    # Use a prefix sum array to optimize range sum calculations
    prefix_sum = [0] * (N + 1)
    for i in range(1, N + 1):
        prefix_sum[i] = prefix_sum[i - 1] + profits[i - 1]

    for i in range(1, N + 1):
        # Option 1: Don't take the current project
        dp[i] = dp[i - 1]
        # Option 2: Take the current project and add its profit
        if i >= K + 1:
            dp[i] = max(dp[i], dp[i - (K + 1)] + profits[i - 1])
        else:
            dp[i] = max(dp[i], profits[i - 1])

    return dp[N]

if __name__ == '__main__':
    n, k = map(int, input().split())
    arr = [int(input()) for _ in range(n)]
    res = max_profit(n,k,arr)
    print(res)