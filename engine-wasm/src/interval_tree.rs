//! 1D Interval Tree for high-frequency spatio-temporal queries.
//!
//! Indexes long-span oral traditions and mythic epochs [epoch_start, epoch_end]
//! allowing discrete temporal queries in O(log N + K) time.

#[derive(Clone, Debug)]
pub struct IntervalEntry {
    pub index: usize,
    pub start: i32,
    pub end: i32,
}

#[derive(Clone, Debug)]
pub struct IntervalNode {
    pub center: i32,
    pub left: Option<Box<IntervalNode>>,
    pub right: Option<Box<IntervalNode>>,
    /// Intervals containing `center`, sorted by start ascending
    pub by_start: Vec<IntervalEntry>,
    /// Intervals containing `center`, sorted by end descending
    pub by_end: Vec<IntervalEntry>,
    /// Maximum upper bound in this subtree
    pub max_end: i32,
}

#[derive(Clone, Debug, Default)]
pub struct IntervalTree {
    root: Option<Box<IntervalNode>>,
    size: usize,
}

impl IntervalTree {
    pub fn new() -> Self {
        Self {
            root: None,
            size: 0,
        }
    }

    pub fn len(&self) -> usize {
        self.size
    }

    pub fn is_empty(&self) -> bool {
        self.size == 0
    }

    /// Builds a balanced interval tree from a collection of intervals.
    pub fn build(mut entries: Vec<IntervalEntry>) -> Self {
        let size = entries.len();
        if entries.is_empty() {
            return Self::new();
        }
        let root = Self::build_recursive(&mut entries);
        Self { root, size }
    }

    fn build_recursive(entries: &mut [IntervalEntry]) -> Option<Box<IntervalNode>> {
        if entries.is_empty() {
            return None;
        }

        // Find endpoints and pick center as midpoint of range
        let mut min_val = i32::MAX;
        let mut max_val = i32::MIN;
        for e in entries.iter() {
            if e.start < min_val {
                min_val = e.start;
            }
            if e.end > max_val {
                max_val = e.end;
            }
        }

        let center = min_val + (max_val - min_val) / 2;

        let mut left_entries: Vec<IntervalEntry> = Vec::new();
        let mut right_entries: Vec<IntervalEntry> = Vec::new();
        let mut center_entries: Vec<IntervalEntry> = Vec::new();

        for e in entries.iter() {
            if e.end < center {
                left_entries.push(e.clone());
            } else if e.start > center {
                right_entries.push(e.clone());
            } else {
                center_entries.push(e.clone());
            }
        }

        // Sort center intervals
        let mut by_start = center_entries.clone();
        by_start.sort_by_key(|e| e.start);

        let mut by_end = center_entries;
        by_end.sort_by_key(|e| -e.end);

        let left_node = Self::build_recursive(&mut left_entries);
        let right_node = Self::build_recursive(&mut right_entries);

        let mut subtree_max = max_val;
        if let Some(ref l) = left_node {
            if l.max_end > subtree_max {
                subtree_max = l.max_end;
            }
        }
        if let Some(ref r) = right_node {
            if r.max_end > subtree_max {
                subtree_max = r.max_end;
            }
        }

        Some(Box::new(IntervalNode {
            center,
            left: left_node,
            right: right_node,
            by_start,
            by_end,
            max_end: subtree_max,
        }))
    }

    /// Queries all interval indices that overlap the specified year (i.e. start <= year <= end).
    pub fn query_point(&self, year: i32) -> Vec<usize> {
        let mut results = Vec::new();
        if let Some(ref node) = self.root {
            Self::query_recursive(node, year, &mut results);
        }
        results
    }

    fn query_recursive(node: &IntervalNode, year: i32, results: &mut Vec<usize>) {
        if year < node.center {
            // Check center intervals starting on or before `year`
            for e in &node.by_start {
                if e.start <= year {
                    results.push(e.index);
                } else {
                    break;
                }
            }
            if let Some(ref left) = node.left {
                Self::query_recursive(left, year, results);
            }
        } else if year > node.center {
            // Check center intervals ending on or after `year`
            for e in &node.by_end {
                if e.end >= year {
                    results.push(e.index);
                } else {
                    break;
                }
            }
            if let Some(ref right) = node.right {
                Self::query_recursive(right, year, results);
            }
        } else {
            // Exactly equal to center - all center intervals overlap
            for e in &node.by_start {
                results.push(e.index);
            }
            // Check both subtrees if they could contain overlapping intervals
            if let Some(ref left) = node.left {
                Self::query_recursive(left, year, results);
            }
            if let Some(ref right) = node.right {
                Self::query_recursive(right, year, results);
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_empty_tree() {
        let tree = IntervalTree::new();
        assert_eq!(tree.query_point(100).len(), 0);
    }

    #[test]
    fn test_interval_tree_point_query() {
        let entries = vec![
            IntervalEntry { index: 0, start: -2100, end: -1200 }, // Gilgamesh
            IntervalEntry { index: 1, start: -1800, end: -1100 }, // Enuma Elish
            IntervalEntry { index: 2, start: -800, end: -700 },   // Iliad
            IntervalEntry { index: 3, start: 800, end: 1250 },    // Ragnarok
        ];

        let tree = IntervalTree::build(entries);
        assert_eq!(tree.len(), 4);

        // At -1500 BCE: both Gilgamesh and Enuma Elish are active
        let mut active = tree.query_point(-1500);
        active.sort();
        assert_eq!(active, vec![0, 1]);

        // At -1200 BCE: Gilgamesh boundary, Enuma Elish active
        let mut active_1200 = tree.query_point(-1200);
        active_1200.sort();
        assert_eq!(active_1200, vec![0, 1]);

        // At -750 BCE: Iliad active
        let active_750 = tree.query_point(-750);
        assert_eq!(active_750, vec![2]);

        // At 1000 CE: Ragnarok active
        let active_1000 = tree.query_point(1000);
        assert_eq!(active_1000, vec![3]);

        // At 0 CE: none active in this small subset
        let active_0 = tree.query_point(0);
        assert_eq!(active_0.len(), 0);
    }
}
